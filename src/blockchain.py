import logging
import requests
from requests import Response


logger = logging.getLogger('root')


class BitcoinAPI:
    def __init__(self):
        self.url: str = "https://api.blockchain.com/v3/exchange"

    def get(self, end_point) -> Response:
        logger.info(f"Request - {self.url + end_point}")
        response = requests.get(url=self.url + end_point)
        logger.info(f"Response {response.status_code} - {response.json()}")
        return response


class BlockChain(BitcoinAPI):
    # async def check(self):
    #     for x in range(20):
    #         print(x)
    #         await asyncio.sleep(1)
    def get_currency(self, end_point: str) -> str:
        return "{:,}".format(self.get(end_point).json()["last_trade_price"])

    def price_bitcoin(self) -> str:
        return self.get_currency(end_point="/tickers/BTC-USD")

    def price_ethereum(self) -> str:
        return self.get_currency(end_point="/tickers/ETH-USD")

    def price_litecoin(self) -> str:
        return self.get_currency(end_point="/tickers/LTC-USD")

    def price_dogecoin(self) -> str:
        return self.get_currency(end_point="/tickers/DOGE-USD")

    def price_cardano(self) -> str:
        return self.get_currency(end_point="/tickers/ADA-USD")
