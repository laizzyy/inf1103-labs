
import unittest
import tempfile
import os
from contextlib import redirect_stdout
from io import StringIO

from inventory_manager import Supplier, Inventory, load_products


class TestCSVLoader(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier(
            "S001", "ABC Supplies", "abc@example.com"
        )

    def test_valid_and_invalid_rows(self):
        inventory = Inventory()
        output = StringIO()

        with redirect_stdout(output):
            load_products("products.csv", inventory, self.supplier)

        self.assertEqual(len(inventory.products), 3)
        self.assertIn("3 products loaded.", output.getvalue())
        self.assertIn("Skipping row 4", output.getvalue())
        self.assertIn("Skipping row 5", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())

    def test_missing_file(self):
        inventory = Inventory()
        output = StringIO()

        with tempfile.TemporaryDirectory() as folder:
            missing_path = os.path.join(folder, "missing.csv")

            with redirect_stdout(output):
                load_products(missing_path, inventory, self.supplier)

        self.assertIn("Products file not found:", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())
        self.assertEqual(len(inventory.products), 0)


if __name__ == "__main__":
    unittest.main()
