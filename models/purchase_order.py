from db.database import get_connection

def create_purchase_order(product_id, supplier_name, 
                           quantity_ordered, notes=""):
    if quantity_ordered <= 0:
        print("Error: quantity must be greater than zero.")
        return
    if not supplier_name:
        print("Error: supplier name cannot be empty.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Check product exists
    cursor.execute("SELECT name FROM products WHERE id = ?", 
                   (product_id,))
    product = cursor.fetchone()

    if not product:
        print(f"Error: product ID {product_id} not found.")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO purchase_orders 
        (product_id, supplier_name, quantity_ordered, notes)
        VALUES (?, ?, ?, ?)
    """, (product_id, supplier_name, quantity_ordered, notes))

    conn.commit()
    po_id = cursor.lastrowid
    conn.close()

    print(f"✅ Purchase Order #{po_id} created for "
          f"'{product[0]}' — {quantity_ordered} units "
          f"from {supplier_name}")
    return po_id

def get_all_purchase_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            po.id,
            p.name,
            po.supplier_name,
            po.quantity_ordered,
            po.status,
            po.created_at
        FROM purchase_orders po
        JOIN products p ON po.product_id = p.id
        ORDER BY po.created_at DESC
    """)

    orders = cursor.fetchall()
    conn.close()
    return orders

def update_po_status(po_id, new_status):
    valid_statuses = ['DRAFT', 'SUBMITTED', 
                      'APPROVED', 'ORDERED', 'RECEIVED']

    if new_status not in valid_statuses:
        print(f"Error: invalid status '{new_status}'.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM purchase_orders WHERE id = ?",
                   (po_id,))
    po = cursor.fetchone()

    if not po:
        print(f"Error: Purchase Order #{po_id} not found.")
        conn.close()
        return

    cursor.execute("""
        UPDATE purchase_orders SET status = ? WHERE id = ?
    """, (new_status, po_id))

    conn.commit()
    conn.close()
    print(f"✅ PO #{po_id} status updated to '{new_status}'")
    
def po_exists_for_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM purchase_orders
        WHERE product_id = ?
        AND status NOT IN ('RECEIVED', 'CANCELLED')
    """, (product_id,))

    row = cursor.fetchone()
    conn.close()

    return row is not None  # True if PO exists, False if not