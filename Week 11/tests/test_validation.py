
import unittest

from inventory_manager import Supplier, PhysicalProduct, OrderLine


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier(
            "S001", "ABC Supplies", "abc@example.com"
        )
        self.product = PhysicalProduct(
            "P001", "Desk", 250.0, 10, 5.0, self.supplier
        )

    def test_zero_price(self):
        with self.assertRaises(ValueError):
            PhysicalProduct(
                "P002", "Invalid", 0, 10, 2.0, self.supplier
            )

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            PhysicalProduct(
                "P003", "Invalid", -5, 10, 2.0, self.supplier
            )

    def test_negative_stock(self):
        with self.assertRaises(ValueError):
            PhysicalProduct(
                "P004", "Invalid", 10, -1, 2.0, self.supplier
            )

    def test_negative_stock_update(self):
        with self.assertRaises(ValueError):
            self.product.update_stock(-1)

    def test_zero_quantity(self):
        with self.assertRaises(ValueError):
            OrderLine(self.product, 0)


if __name__ == "__main__":
    unittest.main()
