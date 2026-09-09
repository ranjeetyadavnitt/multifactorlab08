import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secureshop.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer',
            failed_attempts INTEGER DEFAULT 0,
            locked_until TEXT DEFAULT NULL,
            mfa_enabled INTEGER DEFAULT 1,
            mfa_secret TEXT DEFAULT NULL,
            mfa_backup_codes TEXT DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Migrate existing users table schema if columns are absent
    cursor.execute("PRAGMA table_info(users)")
    existing_cols = [c[1] for c in cursor.fetchall()]
    if 'mfa_enabled' not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN mfa_enabled INTEGER DEFAULT 1")
    if 'mfa_secret' not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN mfa_secret TEXT DEFAULT NULL")
    if 'mfa_backup_codes' not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN mfa_backup_codes TEXT DEFAULT NULL")

    # Create Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            description TEXT,
            icon TEXT
        )
    ''')

    # Create Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            category_id INTEGER NOT NULL,
            short_desc TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 10,
            rating REAL DEFAULT 5.0,
            reviews_count INTEGER DEFAULT 0,
            badge TEXT,
            image_url TEXT,
            is_featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    # Create Cart Items table (handles both logged-in users and guest sessions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        )
    ''')

    # Create Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            shipping_address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            country TEXT NOT NULL DEFAULT 'United States',
            subtotal REAL NOT NULL,
            discount_amount REAL DEFAULT 0.0,
            shipping_fee REAL DEFAULT 0.0,
            tax_amount REAL DEFAULT 0.0,
            total_amount REAL NOT NULL,
            coupon_code TEXT,
            payment_method TEXT NOT NULL,
            payment_status TEXT NOT NULL DEFAULT 'Completed',
            order_status TEXT NOT NULL DEFAULT 'Processing',
            tracking_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create Order Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price_each REAL NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # Create Coupons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount_percent INTEGER NOT NULL,
            description TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')

    # Create Audit Logs table for security monitoring
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            event_type TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed Categories if empty
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        categories = [
            ('Hardware Security', 'hardware-security', 'Physical security keys, authenticators, and biometric devices', 'fas fa-key'),
            ('Encrypted Storage', 'encrypted-storage', 'Hardware-encrypted SSDs, USB drives, and cold storage', 'fas fa-hdd'),
            ('Network Defense', 'network-defense', 'Hardware firewalls, secure routers, and VPN appliances', 'fas fa-shield-alt'),
            ('Privacy & Surveillance Defense', 'privacy-defense', 'Faraday shields, data blockers, and webcam covers', 'fas fa-user-secret')
        ]
        cursor.executemany(
            "INSERT INTO categories (name, slug, description, icon) VALUES (?, ?, ?, ?)",
            categories
        )

    # Seed Products if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        products = [
            (
                'TitanKey Ultra FIDO2',
                'titankey-ultra-fido2',
                1,
                'Next-gen FIDO2/WebAuthn USB-C & NFC hardware authenticator token.',
                'The TitanKey Ultra is an enterprise-grade hardware security key featuring FIDO2, WebAuthn, and U2F compliance with dual USB-C and NFC connectivity. Built with a tamper-resistant secure element (EAL6+) certified to resist physical and side-channel extraction attacks. Eliminates phishing and account takeover risks.',
                59.99,
                45,
                4.9,
                128,
                'Best Seller',
                '/static/images/products/titankey.svg',
                1
            ),
            (
                'AegisVault Pro 1TB Encrypted SSD',
                'aegisvault-pro-1tb-ssd',
                2,
                'Military-grade hardware-encrypted portable SSD with physical numeric keypad.',
                'AegisVault Pro offers real-time XTS-AES 256-bit hardware encryption with zero software requirements. Features a wear-resistant physical alphanumeric keypad for PIN entry (7-15 digits), auto-lock on disconnect, and brute-force self-destruct mechanism after 10 invalid PIN attempts.',
                189.99,
                22,
                4.8,
                84,
                'Military Grade',
                '/static/images/products/aegisvault.svg',
                1
            ),
            (
                'IronWall Gigabit VPN Router',
                'ironwall-gigabit-vpn-router',
                3,
                'Air-gapped dual-core hardware VPN gateway with WireGuard & OpenVPN native support.',
                'IronWall is an open-architecture security gateway engineered for impenetrable home and office network protection. Features native WireGuard throughput up to 900 Mbps, customizable DNS-over-HTTPS sinkholes for ad/malware blocking, and physical killswitch toggle.',
                149.00,
                18,
                4.9,
                96,
                'Top Rated',
                '/static/images/products/ironwall.svg',
                1
            ),
            (
                'CipherShield Faraday Laptop Sleeve',
                'ciphershield-faraday-laptop-sleeve',
                4,
                'EMP and RF signal-blocking Faraday enclosure for 13-16 inch laptops.',
                'Engineered with dual-layer conductive metallic fabric providing 90dB+ shielding attenuation across 10MHz to 10GHz. Completely isolates laptops, tablets, and phones from WiFi, Cellular (5G), Bluetooth, GPS, and RFID tracking and remote tampering.',
                44.50,
                60,
                4.7,
                53,
                'Essential',
                '/static/images/products/faraday.svg',
                1
            ),
            (
                'PrivaShield Cam & Mic Lockdown Pack',
                'privashield-cam-mic-lockdown-pack',
                4,
                'Precision mechanical webcam sliders and 3.5mm acoustic audio blockers.',
                'Complete hardware-level physical privacy kit. Includes 4 ultra-slim metallic webcam sliders with 3M adhesive backing and 2 acoustic audio jack mic silencer plugs that force hardware microphone circuits into mute mode.',
                16.99,
                150,
                4.6,
                210,
                'Popular',
                '/static/images/products/privashield.svg',
                0
            ),
            (
                'YubiToken Dual-Interface NFC',
                'yubitoken-dual-interface-nfc',
                1,
                'Multi-protocol security key supporting Smart Card (PIV) and OpenPGP.',
                'Compact IP68 water and crush-resistant security token designed for high-assurance enterprise authentication. Supports PIV smart card functionality, OpenPGP 4096-bit RSA keys, TOTP/HOTP authenticator, and FIDO2 passwordless login.',
                69.00,
                35,
                5.0,
                77,
                'Enterprise',
                '/static/images/products/yubitoken.svg',
                1
            ),
            (
                'DarkShield 256GB Keypad Flash Drive',
                'darkshield-256gb-flash-drive',
                2,
                'Rugged aluminum waterproof USB 3.2 drive with on-device crypto engine.',
                'Zero-footprint portable storage featuring on-the-fly AES-256 CBC encryption. An internal rechargeable battery allows pre-unlocking before insertion into any OS (Windows, macOS, Linux, Android) without running third-party software or drivers.',
                89.95,
                30,
                4.8,
                42,
                'Rugged',
                '/static/images/products/darkshield.svg',
                0
            ),
            (
                'SentriGate Managed Firewall Appliance',
                'sentrigate-managed-firewall',
                3,
                'Quad-port multi-gigabit intrusion prevention system with deep packet inspection.',
                'SentriGate delivers high-performance stateful inspection, Snort-compatible IDS/IPS intrusion prevention, and real-time geo-blocking. Equipped with 4x 2.5GbE Intel i226-V ports and an aluminum fanless silent chassis.',
                349.00,
                12,
                4.9,
                31,
                'Pro Defense',
                '/static/images/products/sentrigate.svg',
                1
            ),
            (
                'BlackHole USB Data Blocker (3-Pack)',
                'blackhole-usb-data-blocker-3pack',
                4,
                'Defends against juice jacking and malicious USB malware at public chargers.',
                'Physically isolates the data transfer pins (D+ and D-) on standard USB connections while allowing maximum power delivery (up to 20V/5A with PD handshake bypass). Essential travel protection for airports, hotels, and cafes.',
                21.99,
                120,
                4.9,
                340,
                'Must Have',
                '/static/images/products/datablocker.svg',
                0
            ),
            (
                'CryptoVault Steel Seed Backup Cassette',
                'cryptovault-steel-seed-backup',
                2,
                'Indestructible 304 stainless steel seed storage resistant to fire, water, and corrosion.',
                'Safeguard your 12-24 word recovery phrases against catastrophes. Engineered from solid grade-304 stainless steel with a melting point exceeding 2500°F (1370°C). Resistant to crushing, flood, and acid exposure.',
                79.00,
                40,
                5.0,
                95,
                'Indestructible',
                '/static/images/products/cryptovault.svg',
                0
            ),
            (
                'AirGate Zero-Trust Cold Wallet',
                'airgate-zero-trust-cold-wallet',
                1,
                '100% air-gapped cryptographic signing device with QR code optical bridge.',
                'The ultimate non-custodial hardware signer with NO Bluetooth, NO WiFi, NO cellular, and NO USB data lines. Interacts with companion software purely via camera and encrypted animated QR codes on a high-res color display.',
                169.00,
                25,
                4.9,
                64,
                'Air-Gapped',
                '/static/images/products/airgate.svg',
                1
            ),
            (
                'TorBouncer Portable Privacy Router',
                'torbouncer-portable-privacy-router',
                3,
                'Pocket-sized battery-powered Tor gateway with built-in Wi-Fi repeater mode.',
                'Automatically routes all connected client traffic through the Tor onion network or custom WireGuard tunnel. Includes 5000mAh battery for 8+ hours of portable anonymous browsing while on public networks.',
                119.00,
                28,
                4.7,
                49,
                'Portable',
                '/static/images/products/torbouncer.svg',
                0
            )
        ]
        cursor.executemany('''
            INSERT INTO products (
                name, slug, category_id, short_desc, description, price, stock, rating, reviews_count, badge, image_url, is_featured
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)

    # Seed Coupons if empty
    cursor.execute("SELECT COUNT(*) FROM coupons")
    if cursor.fetchone()[0] == 0:
        coupons = [
            ('SECURE20', 20, '20% off total order - Secure Launch Promo'),
            ('CYBER10', 10, '10% off any order - Cybersecurity Month Discount'),
            ('FREESHIP', 100, 'Free Shipping on all security gear') # Special handling for shipping
        ]
        cursor.executemany("INSERT INTO coupons (code, discount_percent, description) VALUES (?, ?, ?)", coupons)

    # Seed Users (Admin & Demo Customer) if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        admin_pass = generate_password_hash('Admin@123456!')
        user_pass = generate_password_hash('Customer@123456!')

        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@secureshop.io', admin_pass, 'admin'))

        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', ('cyberuser', 'user@secureshop.io', user_pass, 'customer'))

        # Add initial audit log entry
        cursor.execute('''
            INSERT INTO audit_logs (username, event_type, ip_address, details)
            VALUES (?, ?, ?, ?)
        ''', ('SYSTEM', 'SYSTEM_INITIALIZED', '127.0.0.1', 'SecureShop database schema created and seeded successfully.'))

    # Ensure all users have valid MFA secrets and backup codes initialized
    cursor.execute("SELECT id, username FROM users WHERE mfa_secret IS NULL OR mfa_secret = ''")
    unconfigured_users = cursor.fetchall()
    if unconfigured_users:
        import base64, json, secrets
        for u in unconfigured_users:
            sec = base64.b32encode(secrets.token_bytes(20)).decode('utf-8').replace('=', '')
            backup_list = [f"{secrets.token_hex(2).upper()}-{secrets.token_hex(2).upper()}" for _ in range(8)]
            cursor.execute(
                "UPDATE users SET mfa_enabled = 1, mfa_secret = ?, mfa_backup_codes = ? WHERE id = ?",
                (sec, json.dumps(backup_list), u['id'])
            )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("SecureShop database initialized successfully!")
