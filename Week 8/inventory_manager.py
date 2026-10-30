import json
import os


# =====================================
# PRODUCT CLASS
# =====================================

class Product:
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
            print("----------------------------------------")

    def update_stock(self, product_id, new_stock):
        product = self.search_product(product_id)

        if product:
            product.update_stock(new_stock)
            print("Stock updated successfully!")
        else:
            print("Product not found.")

if __name__ == "__main__":

    inventory = Inventory()

    laptop = Product("P001", "Laptop", 1200.00, 15)
    mouse = Product("P002", "Mouse", 25.50, 40)

    inventory.add_product(laptop)
    inventory.add_product(mouse)

    inventory.display_all()


# =====================================
# TEST PRODUCT CLASS
# =====================================

if __name__ == "__main__":
    laptop = Product("P001", "Laptop", 1200.00, 15)
    laptop.display_information()