import unittest

from src.blockchain import EndPoints


class TestEndPoints(unittest.TestCase):
    def setUp(self):
        self.endpoints = EndPoints()

    def test_attributes(self):
        self.assertIsInstance(self.endpoints.base_url, str)
        self.assertIsInstance(self.endpoints.bitcoin, str)
        self.assertIsInstance(self.endpoints.ethereum, str)
        self.assertIsInstance(self.endpoints.litecoin, str)
        self.assertIsInstance(self.endpoints.dogecoin, str)
        self.assertIsInstance(self.endpoints.cardano, str)
        self.assertIsInstance(self.endpoints.all, str)

