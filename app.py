import os
import time
import json
import secrets
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

from database import init_db, get_db
from security import (
    generate_csrf_token, validate_csrf,
    add_security_headers, audit_log,
    validate_password_strength,
    check_login_lockout, record_failed_login, reset_failed_logins,
    generate_totp_secret, get_totp_code, verify_totp_code,
    generate_backup_codes, generate_otp_code, get_totp_uri, get_qr_code_url
)
import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static'),
    static_url_path='/static'
)

# Use persistent SECRET_KEY from environment or stable fallback so sessions remain valid across serverless instances
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secureshop-defense-key-b9e3a7c18f4d2e5a6c0b')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# Secure cookies when running on Vercel (HTTPS)
app.config['SESSION_COOKIE_SECURE'] = bool(os.environ.get('VERCEL') or os.environ.get('SESSION_COOKIE_SECURE'))
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 7 # 7 days

# Initialize DB on start with graceful exception handling
try:
    with app.app_context():
        init_db()
except Exception as e:
    app.logger.warning(f"Initial DB sync notice: {e}")

# --- Middleware & Hooks ---

_db_initialized = False

@app.before_request
def before_request():
    global _db_initialized
    if not _db_initialized:
        try:
            init_db()
            _db_initialized = True
        except Exception as e:
            app.logger.warning(f"Lazy DB init notice: {e}")

    # Ensure guest session identifier exists
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    
    # Ensure CSRF token is available
    generate_csrf_token()

    # Enforce CSRF protection on mutation requests
    validate_csrf()

@app.after_request
def after_request(response):
    return add_security_headers(response)

@app.context_processor
def inject_context():
    user_id = session.get('user_id')
    sess_id = session.get('session_id')
    cart_count = models.get_cart_count(user_id=user_id, session_id=sess_id)
    categories = models.get_categories()
    return {
        'csrf_token': generate_csrf_token,
        'cart_count': cart_count,
        'categories': categories,
        'current_user': {
            'id': user_id,
            'username': session.get('username'),
            'role': session.get('role'),
            'email': session.get('email')
        }
    }

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please sign in to browse products and access the secure store.', 'info')
            next_target = request.full_path.rstrip('?') if (request.full_path and request.full_path != '/?') else request.path
            return redirect(url_for('login', next=next_target))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id') or session.get('role') != 'admin':
            audit_log('UNAUTHORIZED_ADMIN_ACCESS_ATTEMPT', details=f"Path: {request.path}")
            abort(403, description="Access restricted to authorized cybersecurity administrators.")
        return f(*args, **kwargs)
    return decorated_function

# --- Public & Store Routes ---

@app.route('/')
@login_required
def index():
    featured_products = models.get_products(featured_only=True)
    categories = models.get_categories()
    return render_template(
        'index.html',
        featured_products=featured_products,
        categories=categories
    )

@app.route('/products')
@login_required
def products():
    category_slug = request.args.get('category')
    search_query = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'featured')
    
    current_category = None
    category_id = None
    if category_slug:
        current_category = models.get_category_by_slug(category_slug)
        if current_category:
            category_id = current_category['id']

    product_list = models.get_products(
        category_id=category_id,
        query=search_query if search_query else None,
        sort_by=sort_by
    )

    return render_template(
        'products.html',
        products=product_list,
        current_category=current_category,
        search_query=search_query,
        current_sort=sort_by
    )

@app.route('/product/<slug>')
@login_required
def product_detail(slug):
    product = models.get_product_by_slug(slug)
    if not product:
        abort(404, description="Security hardware item not found.")
    
    related_products = models.get_products(category_id=product['category_id'])
    # Filter out current product
    related_products = [p for p in related_products if p['id'] != product['id']][:4]

    return render_template(
        'product_detail.html',
        product=product,
        related_products=related_products
    )

# --- Cart & Checkout Routes ---

def calculate_cart_totals(cart_items, coupon_code):
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    discount_amount = 0.0
    shipping_fee = 9.99 if (subtotal < 100.0 and subtotal > 0) else 0.0
    coupon = None

    if coupon_code:
        coupon = models.get_coupon(coupon_code)
        if coupon:
            if coupon['code'] == 'FREESHIP':
                shipping_fee = 0.0
            else:
                discount_amount = round(subtotal * (coupon['discount_percent'] / 100.0), 2)

    taxable_amount = max(0.0, subtotal - discount_amount)
    tax_amount = round(taxable_amount * 0.08, 2)
    total = round(max(0.0, subtotal - discount_amount + shipping_fee + tax_amount), 2)

    return {
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'shipping_fee': shipping_fee,
        'tax_amount': tax_amount,
        'total': total,
        'coupon': coupon
    }

@app.route('/cart')
@login_required
def cart_view():
    user_id = session.get('user_id')
    sess_id = session.get('session_id')
    cart_items = models.get_cart_items(user_id=user_id, session_id=sess_id)
    coupon_code = session.get('coupon_code')
    totals = calculate_cart_totals(cart_items, coupon_code)

    return render_template(
        'cart.html',
        cart_items=cart_items,
        subtotal=totals['subtotal'],
        discount_amount=totals['discount_amount'],
        shipping_fee=totals['shipping_fee'],
        tax_amount=totals['tax_amount'],
        total=totals['total'],
        coupon=totals['coupon']
    )

@app.route('/cart/clear', methods=['POST'])
@login_required
def cart_clear():
    user_id = session.get('user_id')
    sess_id = session.get('session_id')
    models.clear_cart(user_id=user_id, session_id=sess_id)
    session.pop('coupon_code', None)
    flash('Cart emptied successfully.', 'info')
    return redirect(url_for('cart_view'))

@app.route('/checkout')
@login_required
def checkout():
    user_id = session.get('user_id')
    sess_id = session.get('session_id')
    cart_items = models.get_cart_items(user_id=user_id, session_id=sess_id)
    if not cart_items:
        flash('Your cart is empty. Please select products first.', 'warning')
        return redirect(url_for('cart_view'))

    coupon_code = session.get('coupon_code')
    totals = calculate_cart_totals(cart_items, coupon_code)

    return render_template(
        'checkout.html',
        cart_items=cart_items,
        subtotal=totals['subtotal'],
        discount_amount=totals['discount_amount'],
        shipping_fee=totals['shipping_fee'],
        tax_amount=totals['tax_amount'],
        total=totals['total'],
        coupon=totals['coupon']
    )

@app.route('/checkout/submit', methods=['POST'])
@login_required
def checkout_submit():
    user_id = session.get('user_id')
    sess_id = session.get('session_id')
    cart_items = models.get_cart_items(user_id=user_id, session_id=sess_id)

    if not cart_items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart_view'))

    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    shipping_address = request.form.get('shipping_address', '').strip()
    city = request.form.get('city', '').strip()
    state = request.form.get('state', '').strip()
    zip_code = request.form.get('zip_code', '').strip()
    country = request.form.get('country', 'United States').strip()
    payment_method = request.form.get('payment_method', 'Credit Card').strip()
    coupon_code = session.get('coupon_code')

    if not all([customer_name, customer_email, shipping_address, city, state, zip_code]):
        flash('Please fill out all required shipping destination fields.', 'error')
        return redirect(url_for('checkout'))

    success, result = models.create_order(
        user_id=user_id,
        customer_name=customer_name,
        customer_email=customer_email,
        shipping_address=shipping_address,
        city=city,
        state=state,
        zip_code=zip_code,
        country=country,
        payment_method=payment_method,
        cart_items=cart_items,
        coupon_code=coupon_code
    )

    if not success:
        flash(f"Order placement failed: {result}", 'error')
        return redirect(url_for('checkout'))

    order_number = result
    # Clear cart and session coupon
    models.clear_cart(user_id=user_id, session_id=sess_id)
    session.pop('coupon_code', None)

    audit_log(
        event_type='ORDER_PLACED',
        details=f"Order {order_number} confirmed. Recipient: {customer_name}, Method: {payment_method}",
        user_id=user_id,
        username=session.get('username', customer_name)
    )

    flash(f"Order {order_number} successfully placed and encrypted!", 'success')
    return redirect(url_for('order_success', order_number=order_number))

@app.route('/order/confirmed/<order_number>')
def order_success(order_number):
    order, items = models.get_order_by_number(order_number)
    if not order:
        abort(404, description="Order receipt not found.")
    return render_template('order_success.html', order=order, items=items)

@app.route('/orders')
@login_required
def orders_history():
    user_orders = models.get_orders_by_user(session['user_id'])
    return render_template('orders.html', orders=user_orders)

# --- Authentication & User Accounts ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        login_input = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not login_input or not password:
            flash('Please provide both username/email and password.', 'error')
            return render_template('login.html')

        # Check account lockout status
        is_locked, lock_message = check_login_lockout(login_input)
        if is_locked:
            audit_log('LOGIN_ATTEMPT_LOCKED_ACCOUNT', details=f"Attempt for locked account: {login_input}")
            flash(lock_message, 'error')
            return render_template('login.html')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (login_input, login_input))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            # Reset failed login password attempts
            reset_failed_logins(user['id'])

            mfa_enabled = bool(user['mfa_enabled']) if ('mfa_enabled' in user.keys() and user['mfa_enabled'] is not None) else True

            # If MFA is required / enabled
            if mfa_enabled:
                otp_code = generate_otp_code()
                session['pending_mfa_user_id'] = user['id']
                session['pending_mfa_username'] = user['username']
                session['pending_mfa_email'] = user['email']
                session['pending_mfa_role'] = user['role']
                session['pending_mfa_otp'] = otp_code
                session['pending_mfa_expiry'] = int(time.time()) + 300  # 5 minutes
                session['pending_mfa_attempts'] = 0
                session['pending_mfa_next'] = request.args.get('next') or request.form.get('next') or ''

                audit_log(
                    'MFA_CHALLENGE_ISSUED',
                    details="Two-factor authentication step requested",
                    user_id=user['id'],
                    username=user['username']
                )

                flash('Password verified! Multi-factor authentication code required.', 'info')
                return redirect(url_for('login_2fa'))

            # Fallback if MFA disabled
            guest_session_id = session.get('session_id')
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user['role']

            if guest_session_id:
                models.migrate_guest_cart_to_user(guest_session_id, user['id'])

            audit_log('LOGIN_SUCCESS', details="User logged in without MFA", user_id=user['id'], username=user['username'])
            flash(f"Welcome back, {user['username']}.", 'success')

            next_url = request.args.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            record_failed_login(login_input)
            audit_log('LOGIN_FAILED', details=f"Failed login attempt for: {login_input}")
            flash('Invalid credentials. Please verify username/email and password.', 'error')

    return render_template('login.html')

@app.route('/login/2fa', methods=['GET', 'POST'])
def login_2fa():
    if session.get('user_id'):
        return redirect(url_for('index'))

    user_id = session.get('pending_mfa_user_id')
    if not user_id:
        flash('No pending multi-factor authentication session found. Please sign in.', 'warning')
        return redirect(url_for('login'))

    user = models.get_user_by_id(user_id)
    if not user:
        session.clear()
        return redirect(url_for('login'))

    totp_secret = user['mfa_secret']
    if not totp_secret:
        totp_secret = generate_totp_secret()
        models.update_user_mfa_settings(user_id, mfa_secret=totp_secret)

    totp_uri = get_totp_uri(user['username'], totp_secret)
    qr_code_url = get_qr_code_url(totp_uri)
    remaining_seconds = max(0, session.get('pending_mfa_expiry', 0) - int(time.time()))
    current_otp = session.get('pending_mfa_otp', '')

    if request.method == 'POST':
        code = request.form.get('code', '').strip().replace(' ', '').replace('-', '')
        backup_code = request.form.get('backup_code', '').strip().upper()

        attempts = session.get('pending_mfa_attempts', 0) + 1
        session['pending_mfa_attempts'] = attempts

        if attempts > 5:
            audit_log('MFA_LOCKED_OUT', details="MFA maximum attempts exceeded", user_id=user['id'], username=user['username'])
            for k in ['pending_mfa_user_id', 'pending_mfa_username', 'pending_mfa_email', 'pending_mfa_role', 'pending_mfa_otp', 'pending_mfa_expiry', 'pending_mfa_attempts', 'pending_mfa_next']:
                session.pop(k, None)
            flash('Maximum verification attempts exceeded. Session terminated for security.', 'error')
            return redirect(url_for('login'))

        is_verified = False
        method_used = None

        # 1. Verify One-Time Security Passcode
        if current_otp and code == current_otp and int(time.time()) <= session.get('pending_mfa_expiry', 0):
            is_verified = True
            method_used = "One-Time Security Passcode"
        # 2. Verify Time-Based One-Time Password (TOTP app)
        elif totp_secret and verify_totp_code(totp_secret, code):
            is_verified = True
            method_used = "Authenticator App (TOTP)"
        # 3. Verify Backup Recovery Code
        elif backup_code and models.consume_backup_code(user['id'], backup_code):
            is_verified = True
            method_used = "Backup Recovery Code"
        elif code and models.consume_backup_code(user['id'], code):
            is_verified = True
            method_used = "Backup Recovery Code"

        if is_verified:
            guest_session_id = session.get('session_id')

            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user['role']

            if guest_session_id:
                models.migrate_guest_cart_to_user(guest_session_id, user['id'])

            next_url = session.get('pending_mfa_next')
            for k in ['pending_mfa_user_id', 'pending_mfa_username', 'pending_mfa_email', 'pending_mfa_role', 'pending_mfa_otp', 'pending_mfa_expiry', 'pending_mfa_attempts', 'pending_mfa_next']:
                session.pop(k, None)

            audit_log('MFA_VERIFIED', details=f"2FA passed successfully via {method_used}", user_id=user['id'], username=user['username'])
            audit_log('LOGIN_SUCCESS', details=f"User authenticated with MFA ({method_used})", user_id=user['id'], username=user['username'])
            flash(f"Welcome back, {user['username']}! Multi-Factor Authentication verified. Identity cryptographically verified via {method_used}.", 'success')

            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            audit_log('MFA_FAILED', details=f"Invalid 2FA token submitted (attempt {attempts}/5)", user_id=user['id'], username=user['username'])
            remaining = max(0, 5 - attempts)
            flash(f"Invalid verification code. Please check your Authenticator app, email passcode, or backup code. ({remaining} attempts remaining)", 'error')

    return render_template(
        'login_2fa.html',
        username=user['username'],
        email=user['email'],
        current_otp=current_otp,
        totp_secret=totp_secret,
        totp_uri=totp_uri,
        qr_code_url=qr_code_url,
        remaining_seconds=remaining_seconds
    )

@app.route('/login/2fa/resend', methods=['POST'])
def login_2fa_resend():
    user_id = session.get('pending_mfa_user_id')
    if not user_id:
        flash('No pending login session found.', 'warning')
        return redirect(url_for('login'))

    new_otp = generate_otp_code()
    session['pending_mfa_otp'] = new_otp
    session['pending_mfa_expiry'] = int(time.time()) + 300
    audit_log('MFA_CODE_RESENT', details="User requested fresh 2FA passcode", user_id=user_id, username=session.get('pending_mfa_username'))
    flash('A fresh 6-digit verification passcode has been generated.', 'success')
    return redirect(url_for('login_2fa'))

@app.route('/login/2fa/cancel', methods=['GET', 'POST'])
def login_2fa_cancel():
    for k in ['pending_mfa_user_id', 'pending_mfa_username', 'pending_mfa_email', 'pending_mfa_role', 'pending_mfa_otp', 'pending_mfa_expiry', 'pending_mfa_attempts', 'pending_mfa_next']:
        session.pop(k, None)
    flash('Authentication cancelled. Returned to login.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('All registration fields are required.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match. Please re-type your master password.', 'error')
            return render_template('register.html')

        is_valid, msg = validate_password_strength(password)
        if not is_valid:
            flash(msg, 'error')
            return render_template('register.html')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            flash('A user with that username or email already exists.', 'error')
            return render_template('register.html')

        password_hash = generate_password_hash(password)
        mfa_sec = generate_totp_secret()
        backup_list = generate_backup_codes(8)

        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, mfa_enabled, mfa_secret, mfa_backup_codes)
            VALUES (?, ?, ?, 'customer', 1, ?, ?)
        ''', (username, email, password_hash, mfa_sec, json.dumps(backup_list)))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        guest_session_id = session.get('session_id')
        session['user_id'] = user_id
        session['username'] = username
        session['email'] = email
        session['role'] = 'customer'

        if guest_session_id:
            models.migrate_guest_cart_to_user(guest_session_id, user_id)

        audit_log('USER_REGISTERED', details="New user account registered with MFA enabled", user_id=user_id, username=username)
        flash('Account registered successfully! Two-Factor Authentication is active.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/account/security', methods=['GET', 'POST'])
@login_required
def account_security():
    user_id = session['user_id']
    user = models.get_user_by_id(user_id)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'toggle_mfa':
            current_state = bool(user['mfa_enabled'])
            new_state = 0 if current_state else 1
            models.update_user_mfa_settings(user_id, mfa_enabled=new_state)
            status_text = "enabled" if new_state else "disabled"
            audit_log('MFA_STATUS_CHANGED', details=f"MFA {status_text}", user_id=user_id, username=user['username'])
            flash(f"Two-Factor Authentication is now {status_text}.", 'success')
            return redirect(url_for('account_security'))

        elif action == 'regenerate_backup_codes':
            models.regenerate_user_backup_codes(user_id)
            audit_log('MFA_BACKUP_CODES_REGENERATED', details="Backup recovery codes regenerated", user_id=user_id, username=user['username'])
            flash("New single-use recovery codes have been generated. Store them safely.", 'success')
            return redirect(url_for('account_security'))

    totp_secret = user['mfa_secret']
    if not totp_secret:
        totp_secret = generate_totp_secret()
        models.update_user_mfa_settings(user_id, mfa_secret=totp_secret)

    totp_uri = get_totp_uri(user['username'], totp_secret)
    qr_code_url = get_qr_code_url(totp_uri)
    try:
        backup_codes = json.loads(user['mfa_backup_codes']) if user['mfa_backup_codes'] else []
    except Exception:
        backup_codes = []

    user_logs = [log for log in models.get_recent_audit_logs(limit=25) if log['username'] == user['username'] or log['user_id'] == user_id]

    return render_template(
        'account_security.html',
        user=user,
        totp_secret=totp_secret,
        totp_uri=totp_uri,
        qr_code_url=qr_code_url,
        backup_codes=backup_codes,
        recent_logs=user_logs[:10]
    )

@app.route('/logout')
def logout():
    username = session.get('username', 'Unknown')
    user_id = session.get('user_id')
    audit_log('LOGOUT', details="User signed out", user_id=user_id, username=username)
    session.clear()
    flash('You have been securely signed out. Session destroyed.', 'info')
    return redirect(url_for('index'))

# --- Admin Portal Routes ---

@app.route('/admin')
@admin_required
def admin_dashboard():
    metrics = models.get_admin_metrics()
    recent_orders = models.get_all_orders()[:6]
    recent_logs = models.get_recent_audit_logs(limit=10)
    return render_template(
        'admin_dashboard.html',
        metrics=metrics,
        recent_orders=recent_orders,
        recent_logs=recent_logs
    )

@app.route('/admin/products')
@admin_required
def admin_products():
    all_products = models.get_products(sort_by='newest')
    categories = models.get_categories()
    return render_template(
        'admin_products.html',
        products=all_products,
        categories=categories
    )

@app.route('/admin/products/save', methods=['POST'])
@admin_required
def admin_product_save():
    product_id = request.form.get('product_id')
    name = request.form.get('name', '').strip()
    slug = request.form.get('slug', '').strip()
    category_id = int(request.form.get('category_id', 1))
    short_desc = request.form.get('short_desc', '').strip()
    description = request.form.get('description', '').strip()
    price = float(request.form.get('price', 0.0))
    stock = int(request.form.get('stock', 0))
    badge = request.form.get('badge', '').strip() or None
    image_url = request.form.get('image_url', '').strip() or '/static/images/products/titankey.svg'
    is_featured = 1 if request.form.get('is_featured') else 0

    product_id_val = int(product_id) if product_id and product_id.isdigit() else None

    models.save_product(
        name=name,
        slug=slug,
        category_id=category_id,
        short_desc=short_desc,
        description=description,
        price=price,
        stock=stock,
        badge=badge,
        image_url=image_url,
        is_featured=is_featured,
        product_id=product_id_val
    )

    action = "Updated" if product_id_val else "Created"
    audit_log('PRODUCT_MODIFIED', details=f"{action} product '{name}' (Slug: {slug})")
    flash(f"Product '{name}' saved successfully!", 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/products/<int:product_id>/delete', methods=['POST'])
@admin_required
def admin_product_delete(product_id):
    prod = models.get_product_by_id(product_id)
    if prod:
        models.delete_product(product_id)
        audit_log('PRODUCT_DELETED', details=f"Deleted product #{product_id} ('{prod['name']}')")
        flash(f"Product '{prod['name']}' deleted.", 'info')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    all_orders = models.get_all_orders()
    return render_template('admin_orders.html', orders=all_orders)

@app.route('/admin/orders/<int:order_id>/update', methods=['POST'])
@admin_required
def admin_order_update(order_id):
    new_status = request.form.get('status')
    tracking_number = request.form.get('tracking_number')

    models.update_order_status(order_id, new_status, tracking_number if tracking_number else None)
    audit_log('ORDER_STATUS_UPDATED', details=f"Order #{order_id} updated to status '{new_status}'")
    flash(f"Order #{order_id} updated successfully.", 'success')

    # Return to previous page or admin orders
    referer = request.referrer
    if referer and ('admin' in referer):
        return redirect(referer)
    return redirect(url_for('admin_orders'))

@app.route('/admin/audit-logs')
@admin_required
def admin_audit_logs():
    logs = models.get_recent_audit_logs(limit=100)
    return render_template('admin_audit_logs.html', logs=logs)

# --- Interactive AJAX REST API Endpoints ---

@app.route('/api/cart/add', methods=['POST'])
def api_cart_add():
    if not session.get('user_id'):
        return jsonify({
            'success': False,
            'message': 'Please authenticate first to add items to your shopping bag.',
            'login_required': True,
            'redirect': url_for('login')
        }), 401

    data = request.get_json() or {}
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({'success': False, 'message': 'Missing product ID'}), 400

    user_id = session.get('user_id')
    sess_id = session.get('session_id')

    success, message = models.add_to_cart(
        product_id=product_id,
        quantity=quantity,
        user_id=user_id,
        session_id=sess_id
    )

    new_count = models.get_cart_count(user_id=user_id, session_id=sess_id)
    return jsonify({
        'success': success,
        'message': message,
        'cart_count': new_count
    })

@app.route('/api/cart/update', methods=['POST'])
def api_cart_update():
    data = request.get_json() or {}
    cart_id = data.get('cart_id')
    quantity = int(data.get('quantity', 1))

    if not cart_id:
        return jsonify({'success': False, 'message': 'Missing cart ID'}), 400

    user_id = session.get('user_id')
    sess_id = session.get('session_id')

    success, message = models.update_cart_item(
        cart_id=cart_id,
        quantity=quantity,
        user_id=user_id,
        session_id=sess_id
    )

    new_count = models.get_cart_count(user_id=user_id, session_id=sess_id)
    return jsonify({
        'success': success,
        'message': message,
        'cart_count': new_count
    })

@app.route('/api/cart/remove', methods=['POST'])
def api_cart_remove():
    data = request.get_json() or {}
    cart_id = data.get('cart_id')

    if not cart_id:
        return jsonify({'success': False, 'message': 'Missing cart ID'}), 400

    user_id = session.get('user_id')
    sess_id = session.get('session_id')

    models.remove_from_cart(cart_id, user_id=user_id, session_id=sess_id)
    new_count = models.get_cart_count(user_id=user_id, session_id=sess_id)

    return jsonify({
        'success': True,
        'message': 'Item removed from cart',
        'cart_count': new_count
    })

@app.route('/api/cart/apply-coupon', methods=['POST'])
def api_apply_coupon():
    data = request.get_json() or {}
    code = data.get('code', '').strip().upper()

    coupon = models.get_coupon(code)
    if not coupon:
        return jsonify({'success': False, 'message': 'Invalid or expired promotional voucher code.'}), 404

    session['coupon_code'] = coupon['code']
    return jsonify({
        'success': True,
        'message': f"Coupon '{coupon['code']}' applied: {coupon['description']}",
        'discount_percent': coupon['discount_percent']
    })

# --- Error Handling ---

@app.errorhandler(403)
def forbidden_error(e):
    return render_template(
        'error.html',
        error_code=403,
        error_title="Access Forbidden",
        error_message=str(getattr(e, 'description', 'Security policy violation. You do not have authorization to access this cryptographic perimeter.'))
    ), 403

@app.errorhandler(404)
def not_found_error(e):
    return render_template(
        'error.html',
        error_code=404,
        error_title="Resource Not Found",
        error_message="The requested secure asset, route, or product identifier cannot be located on this node."
    ), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template(
        'error.html',
        error_code=500,
        error_title="Internal System Anomaly",
        error_message="A server exception was intercepted. Telemetry has been suppressed for privacy."
    ), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting SecureShop on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=True)
