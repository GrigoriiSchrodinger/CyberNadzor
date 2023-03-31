import asyncio
import logging

import requests

from src.bot.send.below import send_message_below
from src.bot.send.higher import send_message_higher
from src.number_formatting import formatting

logger = logging.getLogger('root')


class EndPoints:
    def __init__(self):
        self.base_url: str = "https://api.blockchain.com/v3/exchange"
        self.bitcoin: str = "/tickers/BTC-USD"
        self.ethereum: str = "/tickers/ETH-USD"
        self.litecoin: str = "/tickers/LTC-USD"
        self.dogecoin: str = "/tickers/DOGE-USD"
        self.cardano: str = "/tickers/ADA-USD"
        self.all: str = "/tickers"


class BlockChainAPI(EndPoints):
    def get(self, end_point) -> list | dict:
        url = self.base_url + end_point
        logger.info(f"Request - {url}")
        response = requests.get(url=url)
        if response.status_code != 200:
            logger.error(f"Error {response.status_code} - {response.text}")
            raise Exception("Error fetching data")
        data = response.json()
        logger.info(f"Response {response.status_code} - {data}")
        return data


class BlockChainPrice(BlockChainAPI):
    def get_price(self, end_point: str) -> str:
        price = self.get(end_point=end_point)["last_trade_price"]
        return formatting(price)

    def price_bitcoin(self) -> str:
        return self.get_price(end_point=self.bitcoin)

    def price_ethereum(self) -> str:
        return self.get_price(end_point=self.ethereum)

    def price_litecoin(self) -> str:
        return self.get_price(end_point=self.litecoin)

    def price_dogecoin(self) -> str:
        return self.get_price(end_point=self.dogecoin)

    def price_cardano(self) -> str:
        return self.get_price(end_point=self.cardano)

    def price_all(self):
        return self.get(end_point=self.all)


class BlockChainRaceTrack(BlockChainPrice):
    CURRENCY = [
        "BTC-USD",
        "ETH-USD",
        "LTC-USD",
        "DOGE-USD",
        "ADA-USD",
    ]

    def __init__(self):
        super().__init__()
        from src.loader import db
        self.db = db

    def get_currency_data(self) -> list[dict]:
        """
        Получает данные о ценах криптовалют
        :return: список словарей вида {"currency": str, "price": float}
        """
        all_tickers = self.price_all()
        currency_data = [
            {"currency": ticker["symbol"], "price": ticker["last_trade_price"]}
            for ticker in all_tickers
            if ticker["symbol"] in self.CURRENCY
        ]
        return currency_data

    async def notify_users(self, users_data_higher, users_data_below, currency_data):
        for user_data in users_data_higher:
            for user_currency in currency_data:
                if user_data.get(user_currency["currency"]) and float(user_currency["price"]) >= float(
                        user_data[user_currency["currency"]]):
                    await send_message_higher(
                        id_user=user_data["id_user"],
                        currency=user_currency["currency"],
                        price_currency=user_data[user_currency["currency"]]
                    )
                    self.db.delete_currency(
                        table="higher_track", currency=user_currency["currency"], id_user=user_data["id_user"]
                    )

        for user_data in users_data_below:
            for user_currency in currency_data:
                if user_data.get(user_currency["currency"]) and float(user_currency["price"]) <= float(
                        user_data[user_currency["currency"]]):
                    await send_message_below(
                        id_user=user_data["id_user"],
                        currency=user_currency["currency"],
                        price_currency=user_data[user_currency["currency"]]
                    )
                    self.db.delete_currency(
                        table="below_track", currency=user_currency["currency"], id_user=user_data["id_user"]
                    )

    async def track_crypto(self) -> None:
        """
        Асинхронно отслеживает изменения цен на заданные криптовалюты,
        уведомляя пользователей, если цена достигает заданного уровня
        """
        while True:
            currency_data = self.get_currency_data()
            users_data = self.db.get_users_data()

            users_data_higher = users_data["higher"]
            users_data_below = users_data["below"]

            await self.notify_users(users_data_higher, users_data_below, currency_data)

            await asyncio.sleep(60)
