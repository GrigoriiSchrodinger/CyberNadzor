import asyncio
import logging

import requests

from bot.send.below import send_message_below
from bot.send.higher import send_message_higher
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

        currency = ["BTC-USD", "ETH-USD", "LTC-USD", "DOGE-USD", "ADA-USD"]
        while True:
            currency_data = [
                {"currency": ticker["symbol"], "price": ticker["last_trade_price"]}
                for ticker in self.get(end_point="/tickers")
                if ticker["symbol"] in currency
            ]

            users_data = db.get_users_data()

            users_data_higher = users_data["higher"]
            users_data_below = users_data["below"]

            for user_data in users_data_higher:
                for user_currency in currency_data:
                    if user_data.get(user_currency["currency"]) and user_currency["price"] >= user_data[user_currency["currency"]]:
                        await send_message_higher(
                            id_user=user_data["id_user"],
                            currency=user_currency["currency"],
                            price_currency=user_data[user_currency["currency"]]
                        )
                        db.delete_currency(
                            table="higher_track", currency=user_currency["currency"], id_user=user_data["id_user"]
                        )

            for user_data in users_data_below:
                for user_currency in currency_data:
                    if user_data.get(user_currency["currency"]) and user_currency["price"] <= user_data[user_currency["currency"]]:
                        await send_message_below(
                            id_user=user_data["id_user"],
                            currency=user_currency["currency"],
                            price_currency=user_data[user_currency["currency"]]
                        )
                        db.delete_currency(
                            table="below_track", currency=user_currency["currency"], id_user=user_data["id_user"]
                        )
            await asyncio.sleep(30)

