import json
import os

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, new_stock):
        self.stock = new_stock

    def display_information(self):
        print(f"ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock}")

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def display_all(self):
        for product in self.products:
            product.display_information()

    def search_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product

        return None

    def update_stock(self, product_id, new_stock):
        product = self.search_product(product_id)

        if product:
            product.update_stock(new_stock)
            print("Stock updated successfully!")
        else:
            print("Product not found.")

class PhysicalProduct(Product):

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.weight} kg")

class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.download_size} MB")

laptop = PhysicalProduct("P001", "Laptop", 1200, 15, 2.5)
software = DigitalProduct("P002", "Antivirus", 59.90, 20, 500)

laptop.display_information()
print()
software.display_information()