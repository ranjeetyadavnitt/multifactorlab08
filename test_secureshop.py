import re
import unittest
import models
from app import app

class TestSecureShop(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        from database import get_db
        conn = get_db()
        conn.execute("UPDATE products SET stock = 45 WHERE id = 1")
        conn.commit()
        conn.close()

    def extract_csrf_token(self, html):
        match = re.search(r'name="csrf_token" value="([a-f0-9]+)"', html)
        if match:
            return match.group(1)
        match = re.search(r'name="csrf-token" content="([a-f0-9]+)"', html)
        if match:
            return match.group(1)
        return None

    def login_as_customer(self):
        login_page = self.client.get('/login')
        csrf = self.extract_csrf_token(login_page.data.decode('utf-8'))
        step1 = self.client.post('/login', data={
            'csrf_token': csrf,
            'username': 'user@secureshop.io',
            'password': 'Customer@123456!'
        }, follow_redirects=True)
        otp_match = re.search(r'id="sampleOtpDisplay">(\d{6})</span>', step1.data.decode('utf-8'))
        otp = otp_match.group(1) if otp_match else '123456'
        csrf_2fa = self.extract_csrf_token(step1.data.decode('utf-8'))
        return self.client.post('/login/2fa', data={
            'csrf_token': csrf_2fa,
            'code': otp
        }, follow_redirects=True)

    def test_01_unauthenticated_access_requires_login(self):
        # 1. Unauthenticated request to / redirects to /login
        res_home = self.client.get('/')
        self.assertEqual(res_home.status_code, 302)
        self.assertIn('/login', res_home.headers.get('Location', ''))

        # 2. Unauthenticated request to /products redirects to /login
        res_prod = self.client.get('/products')
        self.assertEqual(res_prod.status_code, 302)
        self.assertIn('/login', res_prod.headers.get('Location', ''))

        # 3. Unauthenticated request to product detail redirects to /login
        res_detail = self.client.get('/product/titankey-ultra-fido2')
        self.assertEqual(res_detail.status_code, 302)
        self.assertIn('/login', res_detail.headers.get('Location', ''))

        # 4. Unauthenticated request to cart redirects to /login
        res_cart = self.client.get('/cart')
        self.assertEqual(res_cart.status_code, 302)
        self.assertIn('/login', res_cart.headers.get('Location', ''))

        # 5. Unauthenticated API cart add returns 401 when CSRF is present
        login_res = self.client.get('/login')
        csrf = self.extract_csrf_token(login_res.data.decode('utf-8'))
        res_api = self.client.post('/api/cart/add', json={'product_id': 1, 'quantity': 1}, headers={'X-CSRF-Token': csrf})
        self.assertEqual(res_api.status_code, 401)

    def test_02_authenticated_homepage_and_security_headers(self):
        # Authenticate first
        self.login_as_customer()

        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'SecureShop', res.data)
        self.assertIn(b'ZERO-TRUST STORE', res.data)
        
        # Verify defensive security headers
        self.assertEqual(res.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(res.headers.get('X-Frame-Options'), 'SAMEORIGIN')
        self.assertEqual(res.headers.get('X-XSS-Protection'), '1; mode=block')
        self.assertIn("default-src 'self'", res.headers.get('Content-Security-Policy', ''))

    def test_03_catalog_and_filters(self):
        # Authenticate first
        self.login_as_customer()

        res = self.client.get('/products')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'TitanKey Ultra FIDO2', res.data)

        # Category filter
        res_cat = self.client.get('/products?category=hardware-security')
        self.assertEqual(res_cat.status_code, 200)
        self.assertIn(b'TitanKey Ultra FIDO2', res_cat.data)

        # Search query
        res_search = self.client.get('/products?q=Faraday')
        self.assertEqual(res_search.status_code, 200)
        self.assertIn(b'Faraday', res_search.data)

        # Sort order
        res_sort = self.client.get('/products?sort=price_asc')
        self.assertEqual(res_sort.status_code, 200)

    def test_04_product_detail(self):
        # Authenticate first
        self.login_as_customer()

        res = self.client.get('/product/titankey-ultra-fido2')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'TitanKey Ultra FIDO2', res.data)
        self.assertIn(b'Verified Cryptographic Specifications', res.data)

        # Invalid product
        res_404 = self.client.get('/product/non-existent-product-xyz')
        self.assertEqual(res_404.status_code, 404)
        self.assertIn(b'404', res_404.data)

    def test_05_csrf_protection_blocked(self):
        # State mutation without CSRF token must fail with 403
        res = self.client.post('/checkout/submit', data={
            'customer_name': 'Attacker',
            'shipping_address': '123 Fake St'
        })
        self.assertEqual(res.status_code, 403)
        self.assertIn(b'CSRF validation failed', res.data)

    def test_06_cart_and_checkout_flow(self):
        # 1. Login as customer
        self.login_as_customer()

        # 2. Get CSRF token from authenticated home page
        home = self.client.get('/')
        csrf = self.extract_csrf_token(home.data.decode('utf-8'))
        self.assertIsNotNone(csrf)

        # 3. Add product to cart via API
        add_res = self.client.post(
            '/api/cart/add',
            headers={'X-CSRF-Token': csrf},
            json={'product_id': 1, 'quantity': 2}
        )
        self.assertEqual(add_res.status_code, 200)
        json_data = add_res.get_json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['cart_count'], 2)

        # 4. View cart
        cart_view = self.client.get('/cart')
        self.assertEqual(cart_view.status_code, 200)
        self.assertIn(b'TitanKey Ultra FIDO2', cart_view.data)

        # 5. Apply promo code
        promo_res = self.client.post(
            '/api/cart/apply-coupon',
            headers={'X-CSRF-Token': csrf},
            json={'code': 'SECURE20'}
        )
        self.assertEqual(promo_res.status_code, 200)
        self.assertTrue(promo_res.get_json()['success'])

        # 6. View checkout page
        checkout_view = self.client.get('/checkout')
        self.assertEqual(checkout_view.status_code, 200)
        self.assertIn(b'End-to-End Encrypted Checkout', checkout_view.data)

        # 7. Submit checkout
        submit_res = self.client.post('/checkout/submit', data={
            'csrf_token': csrf,
            'customer_name': 'Sarah Connor',
            'customer_email': 'sarah@resistance.net',
            'shipping_address': 'Bunker 7, Tech Way',
            'city': 'Cyber City',
            'state': 'NV',
            'zip_code': '89001',
            'country': 'United States',
            'payment_method': 'Credit Card'
        }, follow_redirects=True)

        self.assertEqual(submit_res.status_code, 200)
        self.assertIn(b'Order Successfully Placed & Encrypted', submit_res.data)
        self.assertIn(b'Sarah Connor', submit_res.data)

    def test_06_customer_and_admin_authentication(self):
        login_page = self.client.get('/login')
        csrf = self.extract_csrf_token(login_page.data.decode('utf-8'))

        # Customer login - Step 1: Submit master credentials (triggers 2FA challenge)
        login_step1 = self.client.post('/login', data={
            'csrf_token': csrf,
            'username': 'user@secureshop.io',
            'password': 'Customer@123456!'
        }, follow_redirects=True)
        self.assertEqual(login_step1.status_code, 200)
        self.assertIn(b'Two-Factor Authentication', login_step1.data)

        # Customer login - Step 2: Complete 2FA with generated passcode
        otp_match = re.search(r'id="sampleOtpDisplay">(\d{6})</span>', login_step1.data.decode('utf-8'))
        self.assertIsNotNone(otp_match, "Expected 6-digit 2FA passcode in demo display")
        customer_otp = otp_match.group(1)
        csrf_2fa = self.extract_csrf_token(login_step1.data.decode('utf-8'))

        login_step2 = self.client.post('/login/2fa', data={
            'csrf_token': csrf_2fa,
            'code': customer_otp
        }, follow_redirects=True)
        self.assertEqual(login_step2.status_code, 200)
        self.assertIn(b'cyberuser', login_step2.data)

        # Access orders
        orders_res = self.client.get('/orders')
        self.assertEqual(orders_res.status_code, 200)
        self.assertIn(b'My Security Orders', orders_res.data)

        # Access account security page
        sec_res = self.client.get('/account/security')
        self.assertEqual(sec_res.status_code, 200)
        self.assertIn(b'Security & Authentication Settings', sec_res.data)

        # Logout
        logout_res = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(logout_res.status_code, 200)

        # Get fresh CSRF token after session clear
        login_page_2 = self.client.get('/login')
        csrf_2 = self.extract_csrf_token(login_page_2.data.decode('utf-8'))

        # Admin login - Step 1: Credentials
        admin_step1 = self.client.post('/login', data={
            'csrf_token': csrf_2,
            'username': 'admin@secureshop.io',
            'password': 'Admin@123456!'
        }, follow_redirects=True)
        self.assertEqual(admin_step1.status_code, 200)
        self.assertIn(b'Two-Factor Authentication', admin_step1.data)

        # Admin login - Step 2: 2FA Verification
        admin_otp_match = re.search(r'id="sampleOtpDisplay">(\d{6})</span>', admin_step1.data.decode('utf-8'))
        self.assertIsNotNone(admin_otp_match)
        admin_otp = admin_otp_match.group(1)
        admin_csrf_2fa = self.extract_csrf_token(admin_step1.data.decode('utf-8'))

        admin_login = self.client.post('/login/2fa', data={
            'csrf_token': admin_csrf_2fa,
            'code': admin_otp
        }, follow_redirects=True)
        self.assertEqual(admin_login.status_code, 200)
        self.assertIn(b'Security & Operations Center', admin_login.data)

        # Admin Inventory view
        admin_prods = self.client.get('/admin/products')
        self.assertEqual(admin_prods.status_code, 200)
        self.assertIn(b'Hardware Inventory Management', admin_prods.data)

        # Admin Orders view
        admin_orders = self.client.get('/admin/orders')
        self.assertEqual(admin_orders.status_code, 200)
        self.assertIn(b'Order Processing & Dispatch', admin_orders.data)

        # Admin Audit logs
        admin_logs = self.client.get('/admin/audit-logs')
        self.assertEqual(admin_logs.status_code, 200)
        self.assertIn(b'Security & Access Audit Log', admin_logs.data)

    def test_07_registration_and_password_strength(self):
        page = self.client.get('/register')
        csrf = self.extract_csrf_token(page.data.decode('utf-8'))

        # Weak password (fails security policy)
        weak_res = self.client.post('/register', data={
            'csrf_token': csrf,
            'username': 'newuser1',
            'email': 'new1@test.com',
            'password': 'weak',
            'confirm_password': 'weak'
        })
        self.assertEqual(weak_res.status_code, 200)
        self.assertIn(b'Password must be at least 8 characters long', weak_res.data)

        # Successful registration with strong password
        good_res = self.client.post('/register', data={
            'csrf_token': csrf,
            'username': 'cryptodefender',
            'email': 'crypto@defend.org',
            'password': 'StrongPass123!@#',
            'confirm_password': 'StrongPass123!@#'
        }, follow_redirects=True)
        self.assertEqual(good_res.status_code, 200)
        self.assertIn(b'cryptodefender', good_res.data)

    def test_08_brute_force_lockout(self):
        page = self.client.get('/login')
        csrf = self.extract_csrf_token(page.data.decode('utf-8'))

        test_user = 'user@secureshop.io'
        # Attempt 5 incorrect logins to trigger account lockout
        for i in range(5):
            self.client.post('/login', data={
                'csrf_token': csrf,
                'username': test_user,
                'password': f'WrongPass{i}!'
            })

        # 6th attempt should return lockout message
        lockout_res = self.client.post('/login', data={
            'csrf_token': csrf,
            'username': test_user,
            'password': 'Customer@123456!'
        })
        self.assertEqual(lockout_res.status_code, 200)
        self.assertIn(b'Account temporarily locked due to repeated failed logins', lockout_res.data)

        # Cleanup: reset lockouts so interactive demo accounts remain ready
        from database import get_db
        conn = get_db()
        conn.execute('UPDATE users SET failed_attempts = 0, locked_until = NULL')
        conn.commit()
        conn.close()

    def test_09_mfa_two_factor_authentication_flow(self):
        """Comprehensive verification of MFA/2FA features: TOTP, invalid codes, backup codes, resend."""
        import json
        from security import get_totp_code
        from database import get_db

        login_page = self.client.get('/login')
        csrf = self.extract_csrf_token(login_page.data.decode('utf-8'))

        # Step 1: Login with valid credentials triggers 2FA
        res_step1 = self.client.post('/login', data={
            'csrf_token': csrf,
            'username': 'admin@secureshop.io',
            'password': 'Admin@123456!'
        }, follow_redirects=True)
        self.assertEqual(res_step1.status_code, 200)
        self.assertIn(b'Two-Factor Authentication', res_step1.data)

        csrf_2fa = self.extract_csrf_token(res_step1.data.decode('utf-8'))

        # 1. Test: Invalid 2FA code is rejected
        bad_2fa = self.client.post('/login/2fa', data={
            'csrf_token': csrf_2fa,
            'code': '000000'
        }, follow_redirects=True)
        self.assertEqual(bad_2fa.status_code, 200)
        self.assertIn(b'Invalid verification code', bad_2fa.data)

        # 2. Test: Resend 2FA code generates a fresh code
        resend_res = self.client.post('/login/2fa/resend', data={
            'csrf_token': csrf_2fa
        }, follow_redirects=True)
        self.assertEqual(resend_res.status_code, 200)
        self.assertIn(b'fresh 6-digit verification passcode', resend_res.data)

        # 3. Test: Verify using real TOTP code (RFC 6238)
        conn = get_db()
        user_row = conn.execute("SELECT id, mfa_secret, mfa_backup_codes FROM users WHERE username = 'admin'").fetchone()
        admin_secret = user_row['mfa_secret']
        try:
            backup_codes = json.loads(user_row['mfa_backup_codes']) if user_row['mfa_backup_codes'] else []
        except Exception:
            backup_codes = []
        if not backup_codes:
            backup_codes = models.regenerate_user_backup_codes(user_row['id'])
        conn.close()

        totp_code = get_totp_code(admin_secret)
        csrf_fresh = self.extract_csrf_token(resend_res.data.decode('utf-8'))

        valid_totp_res = self.client.post('/login/2fa', data={
            'csrf_token': csrf_fresh,
            'code': totp_code
        }, follow_redirects=True)
        self.assertEqual(valid_totp_res.status_code, 200)
        self.assertIn(b'Multi-Factor Authentication verified', valid_totp_res.data)
        self.assertIn(b'Security & Operations Center', valid_totp_res.data)

        # Logout
        self.client.get('/logout')

        # 4. Test: Verify using a single-use Backup Recovery Code
        login_p3 = self.client.get('/login')
        csrf_p3 = self.extract_csrf_token(login_p3.data.decode('utf-8'))
        step1_b = self.client.post('/login', data={
            'csrf_token': csrf_p3,
            'username': 'admin@secureshop.io',
            'password': 'Admin@123456!'
        }, follow_redirects=True)

        csrf_b = self.extract_csrf_token(step1_b.data.decode('utf-8'))
        backup_to_use = backup_codes[0]

        backup_res = self.client.post('/login/2fa', data={
            'csrf_token': csrf_b,
            'backup_code': backup_to_use
        }, follow_redirects=True)
        self.assertEqual(backup_res.status_code, 200)
        self.assertIn(b'Identity cryptographically verified', backup_res.data)

        # Verify backup code was consumed (cannot be used a second time)
        conn = get_db()
        updated_codes = json.loads(conn.execute("SELECT mfa_backup_codes FROM users WHERE username = 'admin'").fetchone()['mfa_backup_codes'])
        conn.close()
        self.assertNotIn(backup_to_use, updated_codes)

        # Logout
        self.client.get('/logout')

if __name__ == '__main__':
    unittest.main()
