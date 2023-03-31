import unittest

from src.number_formatting import formatting


class TestNuberFormatting(unittest.TestCase):
    def test_one(self):
        self.assertEqual(formatting("27000"), "27,000")

    def test_two(self):
        self.assertEqual(formatting("27,000"), "27,000")

    def test_three(self):
        self.assertEqual(formatting("27,000.98"), "27,000.98")

    def test_four(self):
        self.assertEqual(formatting("27000.98"), "27,000.98")


if __name__ == "__main__":
    unittest.main()
