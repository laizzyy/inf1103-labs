
import unittest

from inventory_manager import (
    Supplier, PhysicalProduct, Order,
    NoDiscount, PercentageDiscount,
    BulkDiscount, StudentDiscount
)


class TestStrategy(unittest.TestCase):

    def setUp(self):
        supplier = Supplier("S001", "ABC Supplies", "abc@example.com")
        product = PhysicalProduct(
            "P001", "Desk", 250.0, 10, 5.0, supplier
        )

        self.order = Order("O001")
        self.order.add_order_line(product, 1)

    def test_no_discount(self):
        self.assertAlmostEqual(self.order.calculate_total(), 250.0)

    def test_bulk_discount(self):
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertAlmostEqual(self.order.calculate_total(), 230.0)

    def test_percentage_discount(self):
        self.order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(self.order.calculate_total(), 225.0)

    def test_student_discount(self):
        self.order.set_discount(StudentDiscount())
        self.assertAlmostEqual(self.order.calculate_total(), 237.5)


if __name__ == "__main__":
    unittest.main()
