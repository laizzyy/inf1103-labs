
import unittest
from unittest.mock import patch
from io import StringIO

from inventory_manager import get_positive_float


class TestInput(unittest.TestCase):

    @patch("builtins.input", side_effect=["abc", "-5", "12.50"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_repeated_input(self, mock_output, mock_input):
        result = get_positive_float("Price: ")

        self.assertEqual(result, 12.5)
        self.assertIn(
            "Please enter a valid number",
            mock_output.getvalue()
        )
        self.assertIn(
            "Please enter a number greater than zero",
            mock_output.getvalue()
        )


if __name__ == "__main__":
    unittest.main()
