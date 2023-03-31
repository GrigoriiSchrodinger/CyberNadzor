import random

from asset.dialogues import currency_higher
from src.number_formatting import formatting


async def send_message_higher(id_user, price_currency, currency):
    from src.loader import bot
    messages = {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
        "LTC-USD": "Litecoin",
        "DOGE-USD": "Dogecoin",
        "ADA-USD": "Cardano",
    }

    if currency in messages:
        await bot.send_message(
            id_user,
            random.choice(currency_higher).format(currency=messages[currency], price=formatting(price_currency))
        )
