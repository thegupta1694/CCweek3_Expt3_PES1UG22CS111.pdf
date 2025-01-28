import os
import sqlite3


def connect(path="products.db"):
    exists = os.path.exists(path)
    conn = sqlite3.connect(path)
    if not exists:
        create_tables(conn)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            cost REAL NOT NULL,
            qty INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    # Seed initial data (do not modify this section)
    seed_data = [
        ('Backpack', 'A durable and stylish backpack for daily use.', 800.0, 10),
        ('Wireless Mouse', 'A sleek and ergonomic wireless mouse with a long battery life.', 800.0, 20),
        # Add all other initial products here...
    ]
    conn.executemany(
        'INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)', seed_data
    )
    conn.commit()


def list_products():
    """Fetch all products."""
    with connect() as conn:
        cursor = conn.execute('SELECT * FROM products')
        return [dict(row) for row in cursor.fetchall()]


def add_product(product: dict):
    """Add a new product."""
    with connect() as conn:
        conn.execute(
            'INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)',
            (product['name'], product['description'], product['cost'], product['qty'])
        )
        conn.commit()


def get_product(product_id: int):
    """Retrieve a product by its ID."""
    with connect() as conn:
        cursor = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        return dict(product) if product else None


def update_qty(product_id: int, qty: int):
    """Update the quantity of a product."""
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")
    with connect() as conn:
        conn.execute('UPDATE products SET qty = ? WHERE id = ?', (qty, product_id))
        conn.commit()


def delete_product(product_id: int):
    """Delete a product by its ID."""
    with connect() as conn:
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()


def update_product(product_id: int, product: dict):
    """Update product details."""
    with connect() as conn:
        conn.execute(
            'UPDATE products SET name = ?, description = ?, cost = ?, qty = ? WHERE id = ?',
            (product['name'], product['description'], product['cost'], product['qty'], product_id)
        )
        conn.commit()
