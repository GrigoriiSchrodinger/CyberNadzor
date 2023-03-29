import unittest

from src.number_formatting import formatting


class TestNuberFormatting(unittest.TestCase):
    def test_one(self):
        assert formatting("27000") == "27,000"

    def test_two(self):
        assert formatting("27,000") == "27,000"

    def test_three(self):
        assert formatting("27,000.98") == "27,000.98"

    def test_four(self):
        assert formatting("27000.98") == "27,000.98"

    def test_five(self):
        assert formatting("27,5") == "27,500"


if __name__ == "__main__":
    unittest.main()
