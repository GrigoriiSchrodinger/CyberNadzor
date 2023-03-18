import logging
import requests

logger = logging.getLogger('root')


class BitcoinAPI:
    def __init__(self):
        self.url: str = "https://api.blockchain.com/v3/exchange"

    def get(self, end_point):
        logger.info(f"Request - {self.url + end_point}")
        response = requests.get(url=self.url + end_point)
        logger.info(f"Response {response.status_code} - {response.json()}")
        return response


class BlockChain(BitcoinAPI):
    # async def check(self):
    #     for x in range(20):
    #         print(x)
    #         await asyncio.sleep(1)
    def get_currency(self, end_point):
        return "{:,}".format(self.get(end_point).json()["last_trade_price"])

    def price_bitcoin(self):
        return self.get_currency("/tickers/BTC-USD")

    def price_ethereum(self):
        return self.get_currency("/tickers/ETH-USD")

    def price_litecoin(self):
        return self.get_currency("/tickers/LTC-USD")

    def price_dogecoin(self):
        return self.get_currency("/tickers/DOGE-USD")

    def price_cardano(self):
        return self.get_currency("/tickers/ADA-USD")
