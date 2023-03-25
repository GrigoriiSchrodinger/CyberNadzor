import logging

import requests

from src.number_formatting import formatting

logger = logging.getLogger('root')


class BitcoinChainAPI:
    def __init__(self):
        self.url: str = "https://api.blockchain.com/v3/exchange"

    def get(self, end_point) -> dict | list:
        url = self.url + end_point
        logger.info(f"Request - {url}")
        response = requests.get(url=url)
        if response.status_code != 200:
            logger.error(f"Error {response.status_code} - {response.text}")
            raise Exception("Error fetching data")
        data = response.json()
        logger.info(f"Response {response.status_code} - {data}")
        return data


class BlockChainPrice(BitcoinChainAPI):
    def get_currency(self, end_point: str) -> str:
        return formatting(self.get(end_point)["last_trade_price"])

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


class RaceTrack(BlockChainPrice):
    async def track_crypto(self):
        from src.loader import db
        # tickers = self.get(end_point="/tickers")
        # for ticker in tickers:
        #     await asyncio.sleep(1)
        #     print(ticker)
        date = db.get_users_data()
        print(date)
