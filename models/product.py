import sqlite3 
from db.database import get_connection

def add_product(name, category, quantity, threshold, unit):
    if not name or not category or not unit:
        print("Error: name, category and unit cannot be empty.")
        return
    if quantity < 0:
        print("Error: quantity cannot be negative.")
        return
    if threshold <= 0:
        print("Error: threshold must be greater than zero.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO products (name, category, quantity, threshold, unit)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, quantity, threshold, unit))
        conn.commit()
        print(f"Product '{name}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: product '{name}' already exists.")
    finally:
        conn.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_quantity(product_id, amount):
    # amount can be positive (IN) or negative (OUT)
    conn = get_connection()
    cursor = conn.cursor()

    # Check product exists first
    cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    if not row:
        print("Error: product not found.")
        conn.close()
        return

    new_quantity = row[0] + amount

    if new_quantity < 0:
        print("Error: insufficient stock. Operation cancelled.")
        conn.close()
        return

    cursor.execute("""
        UPDATE products SET quantity = ? WHERE id = ?
    """, (new_quantity, product_id))

    conn.commit()
    conn.close()
    print(f"Quantity updated. New quantity: {new_quantity}")



    