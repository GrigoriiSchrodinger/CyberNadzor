from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard():
    bitcoin_button = InlineKeyboardButton("Bitcoin", callback_data="bitcoin_data")
    ethereum_button = InlineKeyboardButton("Ethereum", callback_data="ethereum_data")
    litecoin_button = InlineKeyboardButton("Litecoin", callback_data="litecoin_data")
    dogecoin_button = InlineKeyboardButton("Dogecoin", callback_data="dogecoin_data")
    cardano_button = InlineKeyboardButton("Cardano", callback_data="cardano_data")

    currency_keyboard = InlineKeyboardMarkup().add(
        bitcoin_button,
        ethereum_button,
        litecoin_button,
        dogecoin_button,
        cardano_button,
    )

    return currency_keyboard
