import random

from src.asset.dialogues import currency_below
from src.utils.number_formatting import formatting


async def send_message_below(id_user, price_currency, currency):
    from src.utils.loader import bot
    messages = {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
        "LTC-USD": "Litecoin",
        "DOGE-USD": "Dogecoin",
        "ADA-USD": "Cardano",
    }

    if currency in messages:
        await bot.send_message(
            id_user, random.choice(currency_below).format(currency=messages[currency], price=formatting(price_currency))
        )

