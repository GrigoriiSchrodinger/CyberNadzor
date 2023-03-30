import unittest

from src.blockchain import BitcoinChainAPI


class TestBlockchainAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.blockchain_api = BitcoinChainAPI()

    # def test_one(self):
    #     self.assertEqual(self.blockchain_api.get())


if __name__ == '__main__':
    unittest.main()
