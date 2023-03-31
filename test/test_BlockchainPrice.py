import unittest

from src.blockchain import BlockChainPrice


class TestBlockchainPrice(unittest.TestCase):
    def setUp(self) -> None:
        self.price = BlockChainPrice()

    def test_type_bitcoin(self):
        self.assertIsInstance(self.price.price_bitcoin(), str)

    def test_type_ethereum(self):
        self.assertIsInstance(self.price.price_ethereum(), str)

    def test_type_litecoin(self):
        self.assertIsInstance(self.price.price_litecoin(), str)

    def test_type_dogecoin(self):
        self.assertIsInstance(self.price.price_dogecoin(), str)

    def test_type_cardano(self):
        self.assertIsInstance(self.price.price_cardano(), str)

    def test_type_all(self):
        self.assertIsInstance(self.price.price_all(), list)


if __name__ == '__main__':
    unittest.main()
