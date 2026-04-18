from db.database import initialize_db
from models.product import add_product, get_all_products
from models.stock_movement import record_movement
from engine.alert_engine import check_low_stock
from reports.daily_report import generate_daily_report
from models.purchase_order import (create_purchase_order,
                                    get_all_purchase_orders,
                                    update_po_status,
                                    po_exists_for_product)

initialize_db()

# Check alerts
print()
low_stock = check_low_stock()

# Create POs for low stock products
print("\n📋 CREATING PURCHASE ORDERS:")
print("-" * 50)
for product in low_stock:
    product_id = product[0]
    deficit = product[4] - product[3]

    if po_exists_for_product(product_id):
        print(f"⏭️  PO already exists for product ID {product_id} — skipping.")
    else:
        create_purchase_order(
            product_id=product_id,
            supplier_name="OCP Supplies Ltd",
            quantity_ordered=deficit,
            notes="Auto-generated from alert engine"
        )

# View all POs
print("\n📦 ALL PURCHASE ORDERS:")
print("-" * 50)
for po in get_all_purchase_orders():
    print(po)

# Simulate approval workflow
print("\n🔄 UPDATING PO STATUS:")
print("-" * 50)
update_po_status(1, "SUBMITTED")
update_po_status(1, "APPROVED")
print()
generate_daily_report()

