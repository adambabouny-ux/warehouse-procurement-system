from db.database import get_connection

def check_low_stock():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category, quantity, threshold, unit
        FROM products
        WHERE quantity < threshold
    """)

    low_stock_products = cursor.fetchall()
    conn.close()

    if not low_stock_products:
        print("✅ All products are sufficiently stocked.")
        return []

    print("\n🚨 LOW STOCK ALERT 🚨")
    print("-" * 50)
    for p in low_stock_products:
        id, name, category, quantity, threshold, unit = p
        deficit = threshold - quantity
        print(f"  ❌ {name} ({category})")
        print(f"     Current : {quantity} {unit}")
        print(f"     Minimum : {threshold} {unit}")
        print(f"     Deficit : {deficit} {unit} needed")
        print()

    return low_stock_products