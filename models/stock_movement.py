from db.database import get_connection

def record_movement(product_id, movement_type, quantity, reason=""):
    if movement_type not in ("IN", "OUT"):
        print("Error: movement_type must be IN or OUT.")
        return
    

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
        VALUES (?, ?, ?, ?)
    """, (product_id, movement_type, quantity, reason))

    

    conn.commit()
    conn.close()