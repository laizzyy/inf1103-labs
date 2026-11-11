import json
import os
from abc import ABC, abstractmethod

# =====================================
# ABSTRACT PRODUCT CLASS
# =====================================

class Supplier:
    def __init__(
        self,
        supplier_id: str,
        name: str,
        contact_email: str
    ) -> None:
        self.supplier_id = supplier_id
        self.name = name
        self.contact_email = contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id}")
        print(f"Supplier Name: {self.name}")
        print(f"Email: {self.contact_email}")


class Product(ABC):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier
    ) -> None:
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.supplier: Supplier = supplier

    def update_stock(self, new_stock):
        self.__stock = new_stock

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

        print("\nSupplier Details:")
        self.display_supplier()

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    def display_supplier(self) -> None:
        self.supplier.display_information()

    def get_stock(self):
        return self.__stock

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

    @abstractmethod
    def get_fulfilment_info(self):
        pass

# =====================================
# SHIPPING INTERFACE
# =====================================

class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


# =====================================
# PHYSICAL PRODUCT CLASS
# =====================================

class PhysicalProduct(Product, CanBeShipped):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        weight: float,
        supplier: Supplier
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.weight * 5
    
# =====================================
# DIGITAL PRODUCT CLASS
# =====================================

class DigitalProduct(Product):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        download_size: float,
        supplier: Supplier
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.download_size} MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally."
    
# =====================================
# INVENTORY CLASS
# =====================================

class Inventory:

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.get_product_id() == product_id:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> None:
        product = self.find_product(product_id)

        if product is not None:
            self.products.remove(product)
        else:
            print("Product not found.")

    def update_stock(self, product_id: str, new_stock: int) -> None:
        product = self.find_product(product_id)

        if product is not None:
            product.update_stock(new_stock)
            print("Stock updated successfully!")
        else:
            print("Product not found.")

    def display_all(self) -> None:
        print("\nCurrent Inventory")

        if not self.products:
            print("No products available.")

        for product in self.products:
            print("----------------------------------------")
            product.display_information()
            print(product.get_fulfilment_info())

class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity


class Order:

    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, index: int) -> None:
        if 0 <= index < len(self.order_lines):
            self.order_lines.pop(index)

    def calculate_total(self) -> float:
        total = 0.0

        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()

        return total

    def display_order(self) -> None:
        print(f"\nOrder ID: {self.order_id}")

        for line in self.order_lines:
            print(
                f"{line.product.get_name()} "
                f"x {line.quantity} = "
                f"${line.calculate_subtotal():.2f}"
            )

        print(f"Total: ${self.calculate_total():.2f}")
# =====================================
# LSP AND POLYMORPHISM
# =====================================

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())

# =====================================
# SAVE INVENTORY
# =====================================


def save_inventory(inventory: Inventory) -> None:
    data = []

    for product in inventory.products:
        item = product.to_dict()

        item["supplier"] = {
            "supplier_id": product.supplier.supplier_id,
            "name": product.supplier.name,
            "contact_email": product.supplier.contact_email
        }

        if isinstance(product, PhysicalProduct):
            item["type"] = "physical"
            item["weight"] = product.weight

        elif isinstance(product, DigitalProduct):
            item["type"] = "digital"
            item["download_size"] = product.download_size

        data.append(item)

    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully!")


# =====================================
# LOAD INVENTORY
# =====================================


def load_inventory() -> Inventory:
    inventory = Inventory()

    if not os.path.exists("inventory.json"):
        print("No existing inventory found.")
        return inventory

    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)

        suppliers = {}

        for item in data:
            supplier_data = item.get("supplier", {
                "supplier_id": "S000",
                "name": "Unknown Supplier",
                "contact_email": "unknown@example.com"
            })

            supplier_id = supplier_data["supplier_id"]

            if supplier_id not in suppliers:
                suppliers[supplier_id] = Supplier(
                    supplier_id,
                    supplier_data["name"],
                    supplier_data["contact_email"]
                )

            supplier = suppliers[supplier_id]

            if item.get("type", "physical") == "physical":
                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item.get("weight", 0.0),
                    supplier
                )

            elif item["type"] == "digital":
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["download_size"],
                    supplier
                )

            else:
                print(f"Skipping unknown product type: {item['type']}")
                continue

            inventory.add_product(product)

        print("Inventory loaded successfully!")

    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Error loading inventory: {error}")

    return inventory

# =====================================
# DISPLAY MENU
# =====================================

def display_menu():

    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

# =====================================
# ADD NEW PRODUCT
# =====================================


def add_new_product(inventory: Inventory) -> None:

    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Choose product type: ")

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    if inventory.search_product(product_id):
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return

        # Supplier information
        print("\nSupplier Information")
        supplier_id = input("Supplier ID: ").strip()
        supplier_name = input("Supplier Name: ").strip()
        supplier_email = input("Supplier Email: ").strip()

        if not supplier_id or not supplier_name or not supplier_email:
            print("Supplier information cannot be empty.")
            return

        supplier = Supplier(
            supplier_id,
            supplier_name,
            supplier_email
        )

        if product_type == "1":
            weight = float(input("Weight (kg): "))

            if weight < 0:
                print("Weight cannot be negative.")
                return

            product = PhysicalProduct(
                product_id, name, price, stock, weight, supplier
            )

        else:
            download_size = float(input("Download Size (MB): "))

            if download_size < 0:
                print("Download size cannot be negative.")
                return

            product = DigitalProduct(
                product_id, name, price, stock, download_size, supplier
            )

        inventory.add_product(product)
        print("Product added successfully!")

    except ValueError:
        print("Invalid input. Please enter valid numbers.")


# =====================================
# UPDATE STOCK
# =====================================

def update_product_stock(inventory):

    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ")

    product = inventory.search_product(product_id)

    if product:

        print("Product Found:")
        print("Name:", product.get_name())
        print("Current Stock:", product.get_stock())

        try:
            new_stock = int(input("New Stock Quantity: "))

            if new_stock < 0:
                print("Stock cannot be negative.")
                return

            inventory.update_stock(product_id, new_stock)

        except ValueError:
            print("Invalid stock quantity.")

    else:
        print("Product not found.")


# =====================================
# SEARCH PRODUCT
# =====================================

def search_for_product(inventory):

    print("\nSearch Product")
    product_id = input("Enter Product ID: ")

    product = inventory.search_product(product_id)

    if product:
        print("\nProduct Found:")
        print("----------------------------------------")

        product.display_information()
        print(product.get_fulfilment_info())

        if isinstance(product, CanBeShipped):
            print(
                f"Shipping Cost: "
                f"${product.calculate_shipping_cost():.2f}"
            )

        print("----------------------------------------")

    else:
        print("Product not found.")
    
# =====================================
# MAIN PROGRAM
# =====================================

def main():

    inventory = load_inventory()

    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    while True:

        display_menu()

        option = input("Enter option: ")

        if option == "1":
            inventory.display_all()

        elif option == "2":
            add_new_product(inventory)

        elif option == "3":
            update_product_stock(inventory)

        elif option == "4":
            search_for_product(inventory)

        elif option == "5":
            save_inventory(inventory)

        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

