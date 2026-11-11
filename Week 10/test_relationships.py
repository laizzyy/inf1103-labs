
from inventory_manager import (
    Supplier,
    PhysicalProduct,
    DigitalProduct,
    Inventory,
    Order,
    show_product_details
)


def main():
    supplier = Supplier(
        "S001", "Tech Supplies", "sales@example.com"
    )

    laptop = PhysicalProduct(
        "P001", "Laptop", 1200, 15, 2.5, supplier
    )

    antivirus = DigitalProduct(
        "P002", "Antivirus", 59.90, 20, 500, supplier
    )

    # TEST 1: Association
    print("\n===== ASSOCIATION =====")
    del supplier
    laptop.display_supplier()
    antivirus.display_supplier()

    # TEST 2: Aggregation
    print("\n===== AGGREGATION =====")
    inventory_a = Inventory()
    inventory_b = Inventory()

    inventory_a.add_product(laptop)
    inventory_a.remove_product("P001")

    laptop.display_information()

    inventory_b.add_product(laptop)
    print(
        "Same product transferred:",
        inventory_b.find_product("P001") is laptop
    )

    # TEST 3: Composition
    print("\n===== COMPOSITION =====")
    order1 = Order("O001")
    order2 = Order("O002")

    order1.add_order_line(laptop, 2)
    order1.add_order_line(antivirus, 1)
    order2.add_order_line(laptop, 1)

    order1.display_order()
    order2.display_order()

    print(
        "Different order lines:",
        order1.order_lines[0] is not order2.order_lines[0]
    )

    print(
        "Same product reference:",
        order1.order_lines[0].product is order2.order_lines[0].product
    )

    # TEST 4: LSP
    print("\n===== LSP =====")
    show_product_details(laptop)
    show_product_details(antivirus)

    laptop.update_stock(10)
    antivirus.update_stock(30)

    print("Laptop stock:", laptop.get_stock())
    print("Antivirus stock:", antivirus.get_stock())

    # TEST 5: Polymorphism
    print("\n===== POLYMORPHISM =====")
    inventory = Inventory()

    inventory.add_product(laptop)
    inventory.add_product(antivirus)

    for product in inventory.products:
        show_product_details(product)
        print("--------------------------------")


if __name__ == "__main__":
    main()
