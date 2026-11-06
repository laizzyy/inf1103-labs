from abc import ABC, abstractmethod
import json
import os


# =====================================
# ABSTRACT PRODUCT CLASS
# =====================================

class Product(ABC):

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, new_stock):
        self.__stock = new_stock

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

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

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
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

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
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

    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def search_product(self, product_id):
        for product in self.products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("----------------------------------------")

        if not self.products:
            print("No products available.")

        for product in self.products:
            product.display_information()
            print(product.get_fulfilment_info())

            if isinstance(product, CanBeShipped):
                print(
                    f"Shipping Cost: "
                    f"${product.calculate_shipping_cost():.2f}"
                )

            print("----------------------------------------")

    def update_stock(self, product_id, new_stock):
        product = self.search_product(product_id)

        if product:
            product.update_stock(new_stock)
            print("Stock updated successfully!")
        else:
            print("Product not found.")

# =====================================
# SAVE INVENTORY
# =====================================

def save_inventory(inventory):

    data = []

    for product in inventory.products:
        item = product.to_dict()

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

def load_inventory():

    inventory = Inventory()

    if not os.path.exists("inventory.json"):
        print("No existing inventory found.")
        return inventory

    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Invalid inventory file format.")
            return inventory

        for item in data:
            product_type = item.get("type", "physical")

            if product_type == "physical":
                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item.get("weight", 0.0)
                )

            elif product_type == "digital":
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["download_size"]
                )

            else:
                print("Unknown product type. Skipping.")
                continue

            inventory.add_product(product)

        print("Inventory loaded successfully!")

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
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

def add_new_product(inventory):

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

        if product_type == "1":
            weight = float(input("Weight (kg): "))

            if weight < 0:
                print("Weight cannot be negative.")
                return

            product = PhysicalProduct(
                product_id, name, price, stock, weight
            )

        else:
            download_size = float(input("Download Size (MB): "))

            if download_size < 0:
                print("Download size cannot be negative.")
                return

            product = DigitalProduct(
                product_id, name, price, stock, download_size
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

