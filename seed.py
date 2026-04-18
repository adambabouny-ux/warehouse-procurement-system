from db.database import initialize_db
from models.product import add_product

initialize_db()

add_product("Steel Pipe", "Spare Parts", 50, 100, "pieces")
add_product("Chemical X", "Chemicals", 200, 50, "liters")
add_product("Bolt M10", "Spare Parts", 5, 50, "pieces")

print("✅ Database seeded successfully.")