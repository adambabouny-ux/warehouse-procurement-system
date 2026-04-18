import pandas as pd
from datetime import datetime
from db.database import get_connection

def generate_daily_report():
    conn = get_connection()

    # --- SECTION 1: Stock Summary ---
    stock_data = conn.execute("""
        SELECT id, name, category, quantity, threshold, unit
        FROM products
        ORDER BY name
    """).fetchall()

    stock_df = pd.DataFrame(stock_data, columns=[
        "ID", "Product", "Category", 
        "Quantity", "Threshold", "Unit"
    ])

    # Add status column automatically
    stock_df["Status"] = stock_df.apply(
        lambda row: "🔴 LOW" if row["Quantity"] < row["Threshold"] 
                    else "✅ OK", axis=1
    )

    # --- SECTION 2: Low Stock ---
    low_stock_df = stock_df[stock_df["Status"] == "🔴 LOW"].copy()
    low_stock_df["Deficit"] = (low_stock_df["Threshold"] 
                                - low_stock_df["Quantity"])

    # --- SECTION 3: Purchase Orders ---
    po_data = conn.execute("""
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
    """).fetchall()

    po_df = pd.DataFrame(po_data, columns=[
        "PO#", "Product", "Supplier", 
        "Qty Ordered", "Status", "Created At"
    ])

    conn.close()

    # --- PRINT REPORT ---
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("\n" + "=" * 60)
    print(f"  📊 DAILY WAREHOUSE REPORT — {today}")
    print(f"  OCP Warehouse Management System")
    print("=" * 60)

    print("\n📦 STOCK SUMMARY:")
    print(stock_df.to_string(index=False))

    print(f"\n🚨 LOW STOCK ITEMS ({len(low_stock_df)} alerts):")
    if low_stock_df.empty:
        print("  ✅ No low stock alerts today.")
    else:
        print(low_stock_df[["Product", "Quantity", 
                              "Threshold", "Deficit", 
                              "Unit"]].to_string(index=False))

    print(f"\n📋 PURCHASE ORDERS ({len(po_df)} total):")
    if po_df.empty:
        print("  No purchase orders found.")
    else:
        print(po_df.to_string(index=False))

    print("\n" + "=" * 60)

   # --- EXPORT TO EXCEL ---
    import os
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"reports/dashboard_{timestamp}.xlsx"

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        stock_df.to_excel(writer, sheet_name="Stock Summary", index=False)
        low_stock_df.to_excel(writer, sheet_name="Low Stock Alerts", index=False)
        po_df.to_excel(writer, sheet_name="Purchase Orders", index=False)

    print(f"\n💾 Excel dashboard exported to: {filename}")
    print("=" * 60)

    return stock_df, low_stock_df, po_df