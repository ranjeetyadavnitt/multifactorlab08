import base64
import hashlib
import hmac
import json
import secrets
import struct
import time
import urllib.parse
import re
from datetime import datetime, timedelta
from flask import session, request, abort
from database import get_db

def generate_csrf_token():
    """Generate or retrieve a CSRF token for the current session."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']

def validate_csrf():
    """Validate CSRF token for state-changing HTTP methods."""
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        # Allow checking either form field or header (X-CSRF-Token)
        token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
        if not token or token != session.get('_csrf_token'):
            audit_log(
                event_type='CSRF_VALIDATION_FAILED',
                details=f"Method: {request.method}, Path: {request.path}",
                username=session.get('username', 'Anonymous')
            )
            abort(403, description="CSRF validation failed. Request blocked for security.")

def add_security_headers(response):
    """Add defensive security headers to every HTTP response."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com data:; "
        "img-src 'self' data: https:; "
        "connect-src 'self';"
    )
    return response

def audit_log(event_type, details=None, user_id=None, username=None):
    """Persist high-assurance audit log entries in the database."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Fall back to session if not provided
        if user_id is None and 'user_id' in session:
            user_id = session['user_id']
        if username is None and 'username' in session:
            username = session.get('username', 'Anonymous')
            
        ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_addr and ',' in ip_addr:
            ip_addr = ip_addr.split(',')[0].strip()
            
        user_agent = request.headers.get('User-Agent', 'Unknown')[:250]

        cursor.execute('''
            INSERT INTO audit_logs (user_id, username, event_type, ip_address, user_agent, details)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, event_type, ip_addr, user_agent, details))
        conn.commit()
        conn.close()
    except Exception as e:
        # Prevent audit log failure from breaking application execution
        print(f"[AUDIT LOGGING ERROR] {e}")

def validate_password_strength(password):
    """
    Validate password adheres to security criteria:
    - Minimum 8 characters
    - At least one lowercase and uppercase letter
    - At least one numeric digit
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must include at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must include at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must include at least one number."
    if not re.search(r'[\W_]', password):
        return False, "Password must include at least one special character (!@#$%^&* etc.)."
    return True, "Password meets security requirements."

def check_login_lockout(username):
    """Check if account is temporarily locked out due to brute-force attempts."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT failed_attempts, locked_until FROM users WHERE username = ? OR email = ?', (username, username))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, None

    failed_attempts = row['failed_attempts']
    locked_until_str = row['locked_until']

    if locked_until_str:
        try:
            locked_until = datetime.fromisoformat(locked_until_str)
            if datetime.utcnow() < locked_until:
                remaining_seconds = int((locked_until - datetime.utcnow()).total_seconds())
                minutes = max(1, (remaining_seconds + 59) // 60)
                return True, f"Account temporarily locked due to repeated failed logins. Try again in {minutes} minutes."
        except Exception:
            pass

    return False, None

def record_failed_login(username):
    """Increment failed login counter and lock account if limit reached."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, failed_attempts FROM users WHERE username = ? OR email = ?', (username, username))
    row = cursor.fetchone()

    if row:
        user_id = row['id']
        attempts = row['failed_attempts'] + 1
        locked_until = None
        
        # Lockout for 15 minutes after 5 consecutive failed attempts
        if attempts >= 5:
            locked_until = (datetime.utcnow() + timedelta(minutes=15)).isoformat()
            audit_log('ACCOUNT_LOCKED', f"Account locked after {attempts} failed attempts for {username}", user_id=user_id, username=username)
        
        cursor.execute('''
            UPDATE users 
            SET failed_attempts = ?, locked_until = ? 
            WHERE id = ?
        ''', (attempts, locked_until, user_id))
        conn.commit()
    conn.close()

def reset_failed_logins(user_id):
    """Reset failed login counter upon successful authentication."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

# --- Multi-Factor Authentication (MFA / 2FA) Engine ---

def generate_totp_secret():
    """Generate a standard 32-character Base32 secret string for RFC 6238 TOTP."""
    return base64.b32encode(secrets.token_bytes(20)).decode('utf-8').replace('=', '')

def get_totp_code(secret, intervals_no=None, time_step=30, digits=6):
    """
    Compute current RFC 6238 Time-Based One-Time Password.
    Compatible with Google Authenticator, Microsoft Authenticator, 1Password, Authy.
    """
    if not secret:
        return ""
    if intervals_no is None:
        intervals_no = int(time.time() // time_step)
    
    clean_secret = secret.strip().replace(' ', '').upper()
    missing_padding = len(clean_secret) % 8
    if missing_padding:
        clean_secret += '=' * (8 - missing_padding)
    
    key = base64.b32decode(clean_secret, casefold=True)
    msg = struct.pack('>Q', intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[19] & 15
    code = (struct.unpack('>I', h[offset:offset+4])[0] & 0x7fffffff) % (10 ** digits)
    return f"{code:0{digits}d}"

def verify_totp_code(secret, code, time_step=30, window=1):
    """
    Verify TOTP code within a +/- window time steps to handle slight client clock drift.
    """
    if not secret or not code:
        return False
    code_str = str(code).strip()
    if not code_str.isdigit() or len(code_str) != 6:
        return False
    
    current_interval = int(time.time() // time_step)
    for i in range(-window, window + 1):
        if get_totp_code(secret, current_interval + i) == code_str:
            return True
    return False

def generate_backup_codes(count=8):
    """Generate human-readable single-use backup recovery codes formatted as XXXX-XXXX."""
    codes = []
    for _ in range(count):
        part1 = secrets.token_hex(2).upper()
        part2 = secrets.token_hex(2).upper()
        codes.append(f"{part1}-{part2}")
    return codes

def generate_otp_code():
    """Generate a high-entropy 6-digit one-time security passcode for login verification."""
    return f"{secrets.randbelow(900000) + 100000}"

def get_totp_uri(username, secret, issuer="SecureShop"):
    """Generate otpauth:// URI for authenticator app enrollment."""
    return f"otpauth://totp/{urllib.parse.quote(issuer)}:{urllib.parse.quote(username)}?secret={secret}&issuer={urllib.parse.quote(issuer)}"

def get_qr_code_url(totp_uri):
    """Return URL to render QR code for authenticator app scanning."""
    return f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={urllib.parse.quote(totp_uri)}"

