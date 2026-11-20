
from inventory_manager import Supplier, Inventory, load_products

supplier = Supplier("S001", "ABC Supplies", "abc@example.com")
inventory = Inventory()

print("===== TEST 1: VALID AND INVALID ROWS =====")
load_products("products.csv", inventory, supplier)

print("\n===== TEST 2: MISSING FILE =====")
load_products("missing_products.csv", Inventory(), supplier)
