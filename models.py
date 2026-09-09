import uuid
import json
from database import get_db

def get_categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_category_by_id(category_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_category_by_slug(slug):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories WHERE slug = ?", (slug,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_products(category_id=None, query=None, sort_by='featured', min_price=None, max_price=None, featured_only=False):
    conn = get_db()
    cursor = conn.cursor()

    sql = """
        SELECT p.*, c.name as category_name, c.slug as category_slug
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE 1=1
    """
    params = []

    if category_id:
        sql += " AND p.category_id = ?"
        params.append(category_id)

    if query:
        search_term = f"%{query}%"
        sql += " AND (p.name LIKE ? OR p.short_desc LIKE ? OR p.description LIKE ?)"
        params.extend([search_term, search_term, search_term])

    if min_price is not None:
        sql += " AND p.price >= ?"
        params.append(min_price)

    if max_price is not None:
        sql += " AND p.price <= ?"
        params.append(max_price)

    if featured_only:
        sql += " AND p.is_featured = 1"

    # Sorting
    if sort_by == 'price_asc':
        sql += " ORDER BY p.price ASC"
    elif sort_by == 'price_desc':
        sql += " ORDER BY p.price DESC"
    elif sort_by == 'rating':
        sql += " ORDER BY p.rating DESC"
    elif sort_by == 'newest':
        sql += " ORDER BY p.id DESC"
    else: # Default: featured first, then id desc
        sql += " ORDER BY p.is_featured DESC, p.id DESC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_product_by_id(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, c.name as category_name, c.slug as category_slug
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = ?
    """, (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_product_by_slug(slug):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, c.name as category_name, c.slug as category_slug
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.slug = ?
    """, (slug,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_cart_items(user_id=None, session_id=None):
    """Retrieve cart items joined with product details."""
    conn = get_db()
    cursor = conn.cursor()

    if user_id:
        cursor.execute("""
            SELECT c.id as cart_id, c.quantity, p.*
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
            ORDER BY c.added_at DESC
        """, (user_id,))
    elif session_id:
        cursor.execute("""
            SELECT c.id as cart_id, c.quantity, p.*
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.session_id = ?
            ORDER BY c.added_at DESC
        """, (session_id,))
    else:
        conn.close()
        return []

    rows = cursor.fetchall()
    conn.close()
    return rows

def get_cart_count(user_id=None, session_id=None):
    conn = get_db()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT SUM(quantity) FROM cart_items WHERE user_id = ?", (user_id,))
    elif session_id:
        cursor.execute("SELECT SUM(quantity) FROM cart_items WHERE session_id = ?", (session_id,))
    else:
        conn.close()
        return 0

    count = cursor.fetchone()[0]
    conn.close()
    return count if count else 0

def add_to_cart(product_id, quantity=1, user_id=None, session_id=None):
    conn = get_db()
    cursor = conn.cursor()

    # Check product stock
    cursor.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
    prod = cursor.fetchone()
    if not prod or prod['stock'] < 1:
        conn.close()
        return False, "Product is currently out of stock."

    # Check if item already exists in cart
    if user_id:
        cursor.execute("SELECT id, quantity FROM cart_items WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    else:
        cursor.execute("SELECT id, quantity FROM cart_items WHERE session_id = ? AND product_id = ?", (session_id, product_id))
    
    existing = cursor.fetchone()
    if existing:
        new_qty = min(prod['stock'], existing['quantity'] + quantity)
        cursor.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (new_qty, existing['id']))
    else:
        cursor.execute("""
            INSERT INTO cart_items (user_id, session_id, product_id, quantity)
            VALUES (?, ?, ?, ?)
        """, (user_id, session_id, product_id, min(prod['stock'], quantity)))

    conn.commit()
    conn.close()
    return True, "Added to cart successfully."

def update_cart_item(cart_id, quantity, user_id=None, session_id=None):
    conn = get_db()
    cursor = conn.cursor()

    # Verify ownership and product stock
    if user_id:
        cursor.execute("SELECT c.*, p.stock FROM cart_items c JOIN products p ON c.product_id = p.id WHERE c.id = ? AND c.user_id = ?", (cart_id, user_id))
    else:
        cursor.execute("SELECT c.*, p.stock FROM cart_items c JOIN products p ON c.product_id = p.id WHERE c.id = ? AND c.session_id = ?", (cart_id, session_id))
    
    item = cursor.fetchone()
    if not item:
        conn.close()
        return False, "Cart item not found."

    if quantity <= 0:
        cursor.execute("DELETE FROM cart_items WHERE id = ?", (cart_id,))
    else:
        quantity = min(quantity, item['stock'])
        cursor.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (quantity, cart_id))

    conn.commit()
    conn.close()
    return True, "Cart updated."

def remove_from_cart(cart_id, user_id=None, session_id=None):
    conn = get_db()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("DELETE FROM cart_items WHERE id = ? AND user_id = ?", (cart_id, user_id))
    else:
        cursor.execute("DELETE FROM cart_items WHERE id = ? AND session_id = ?", (cart_id, session_id))
    conn.commit()
    conn.close()
    return True

def clear_cart(user_id=None, session_id=None):
    conn = get_db()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
    elif session_id:
        cursor.execute("DELETE FROM cart_items WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

def migrate_guest_cart_to_user(session_id, user_id):
    """When a guest logs in, transfer their session cart items to their user account."""
    if not session_id or not user_id:
        return
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, quantity FROM cart_items WHERE session_id = ?", (session_id,))
    guest_items = cursor.fetchall()

    for item in guest_items:
        # Check if already in user's cart
        cursor.execute("SELECT id, quantity FROM cart_items WHERE user_id = ? AND product_id = ?", (user_id, item['product_id']))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("UPDATE cart_items SET quantity = quantity + ? WHERE id = ?", (item['quantity'], existing['id']))
        else:
            cursor.execute("INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, item['product_id'], item['quantity']))

    cursor.execute("DELETE FROM cart_items WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

def get_coupon(code):
    if not code:
        return None
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coupons WHERE UPPER(code) = UPPER(?) AND is_active = 1", (code.strip(),))
    coupon = cursor.fetchone()
    conn.close()
    return coupon

def create_order(user_id, customer_name, customer_email, shipping_address, city, state, zip_code, country, payment_method, cart_items, coupon_code=None):
    """Atomic order creation with stock decrement."""
    if not cart_items:
        return False, "Cart is empty."

    conn = get_db()
    cursor = conn.cursor()

    try:
        # Calculate subtotal and verify stock
        subtotal = 0.0
        for item in cart_items:
            # Check current stock from DB
            cursor.execute("SELECT stock FROM products WHERE id = ?", (item['id'],))
            prod = cursor.fetchone()
            if not prod or prod['stock'] < item['quantity']:
                conn.rollback()
                conn.close()
                return False, f"Not enough stock for {item['name']} (Available: {prod['stock'] if prod else 0})."
            subtotal += item['price'] * item['quantity']

        # Calculate discount
        discount_amount = 0.0
        shipping_fee = 9.99 if subtotal < 100.0 else 0.0

        if coupon_code:
            cursor.execute("SELECT * FROM coupons WHERE UPPER(code) = UPPER(?) AND is_active = 1", (coupon_code.strip(),))
            coupon = cursor.fetchone()
            if coupon:
                if coupon['code'] == 'FREESHIP':
                    shipping_fee = 0.0
                else:
                    discount_amount = round(subtotal * (coupon['discount_percent'] / 100.0), 2)

        tax_amount = round((subtotal - discount_amount) * 0.08, 2) # 8% sales tax
        total_amount = round(max(0.0, subtotal - discount_amount + shipping_fee + tax_amount), 2)

        # Generate unique order number
        order_number = f"SEC-{uuid.uuid4().hex[:8].upper()}"
        tracking_number = f"TRK-{uuid.uuid4().hex[:10].upper()}"

        cursor.execute("""
            INSERT INTO orders (
                order_number, user_id, customer_name, customer_email,
                shipping_address, city, state, zip_code, country,
                subtotal, discount_amount, shipping_fee, tax_amount, total_amount,
                coupon_code, payment_method, payment_status, order_status, tracking_number
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Completed', 'Processing', ?)
        """, (
            order_number, user_id, customer_name, customer_email,
            shipping_address, city, state, zip_code, country,
            subtotal, discount_amount, shipping_fee, tax_amount, total_amount,
            coupon_code, payment_method, tracking_number
        ))

        order_id = cursor.lastrowid

        # Insert order items and decrement stock
        for item in cart_items:
            item_total = round(item['price'] * item['quantity'], 2)
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, price_each, quantity, total_price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (order_id, item['id'], item['name'], item['price'], item['quantity'], item_total))

            cursor.execute("""
                UPDATE products SET stock = stock - ? WHERE id = ?
            """, (item['quantity'], item['id']))

        conn.commit()
        conn.close()
        return True, order_number
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, str(e)

def get_order_by_number(order_number):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
    order = cursor.fetchone()
    if not order:
        conn.close()
        return None, []

    cursor.execute("""
        SELECT oi.*, p.image_url, p.slug
        FROM order_items oi
        LEFT JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """, (order['id'],))
    items = cursor.fetchall()
    conn.close()
    return order, items

def get_orders_by_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM orders
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

def get_all_orders():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.*, u.username
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
    """)
    orders = cursor.fetchall()
    conn.close()
    return orders

def update_order_status(order_id, status, tracking_number=None):
    conn = get_db()
    cursor = conn.cursor()
    if tracking_number:
        cursor.execute("UPDATE orders SET order_status = ?, tracking_number = ? WHERE id = ?", (status, tracking_number, order_id))
    else:
        cursor.execute("UPDATE orders SET order_status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()

def get_admin_metrics():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE payment_status = 'Completed'")
    total_revenue = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'customer'")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE stock <= 5")
    low_stock_count = cursor.fetchone()[0]

    conn.close()
    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_customers': total_customers,
        'low_stock_count': low_stock_count
    }

def get_recent_audit_logs(limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT ?", (limit,))
    logs = cursor.fetchall()
    conn.close()
    return logs

def save_product(name, slug, category_id, short_desc, description, price, stock, badge=None, image_url=None, is_featured=0, product_id=None):
    conn = get_db()
    cursor = conn.cursor()
    if product_id:
        cursor.execute("""
            UPDATE products
            SET name = ?, slug = ?, category_id = ?, short_desc = ?, description = ?,
                price = ?, stock = ?, badge = ?, image_url = ?, is_featured = ?
            WHERE id = ?
        """, (name, slug, category_id, short_desc, description, price, stock, badge, image_url, is_featured, product_id))
    else:
        cursor.execute("""
            INSERT INTO products (
                name, slug, category_id, short_desc, description, price, stock, badge, image_url, is_featured
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, slug, category_id, short_desc, description, price, stock, badge, image_url, is_featured))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# --- User & MFA Helper Functions ---

def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_user_by_username_or_email(identifier):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (identifier, identifier))
    row = cursor.fetchone()
    conn.close()
    return row

def update_user_mfa_settings(user_id, mfa_enabled=None, mfa_secret=None, mfa_backup_codes=None):
    conn = get_db()
    cursor = conn.cursor()
    updates = []
    params = []
    if mfa_enabled is not None:
        updates.append("mfa_enabled = ?")
        params.append(1 if mfa_enabled else 0)
    if mfa_secret is not None:
        updates.append("mfa_secret = ?")
        params.append(mfa_secret)
    if mfa_backup_codes is not None:
        updates.append("mfa_backup_codes = ?")
        params.append(json.dumps(mfa_backup_codes) if isinstance(mfa_backup_codes, list) else mfa_backup_codes)
    if updates:
        params.append(user_id)
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()
    conn.close()

def consume_backup_code(user_id, code):
    """
    Check if code is a valid backup recovery code for user.
    If valid, consume (delete) it from the user record and return True.
    """
    user = get_user_by_id(user_id)
    if not user or not user['mfa_backup_codes']:
        return False
    try:
        codes = json.loads(user['mfa_backup_codes'])
    except Exception:
        return False
    clean_code = code.strip().upper()
    if clean_code in codes:
        codes.remove(clean_code)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET mfa_backup_codes = ? WHERE id = ?", (json.dumps(codes), user_id))
        conn.commit()
        conn.close()
        return True
    return False

def regenerate_user_backup_codes(user_id):
    """Generate 8 fresh single-use backup recovery codes for user."""
    from security import generate_backup_codes
    codes = generate_backup_codes(count=8)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET mfa_backup_codes = ? WHERE id = ?", (json.dumps(codes), user_id))
    conn.commit()
    conn.close()
    return codes

