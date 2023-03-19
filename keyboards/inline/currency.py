from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_price():
    bitcoin_button = InlineKeyboardButton("Bitcoin", callback_data="bitcoin_price")
    ethereum_button = InlineKeyboardButton("Ethereum", callback_data="ethereum_price")
    litecoin_button = InlineKeyboardButton("Litecoin", callback_data="litecoin_price")
    dogecoin_button = InlineKeyboardButton("Dogecoin", callback_data="dogecoin_price")
    cardano_button = InlineKeyboardButton("Cardano", callback_data="cardano_price")

    keyboard = InlineKeyboardMarkup().add(
        bitcoin_button,
        ethereum_button,
        litecoin_button,
        dogecoin_button,
        cardano_button,
    )

    return keyboard


def keyboard_tracks():
    bitcoin_button = InlineKeyboardButton("Bitcoin", callback_data="bitcoin_tracks")
    ethereum_button = InlineKeyboardButton("Ethereum", callback_data="ethereum_tracks")
    litecoin_button = InlineKeyboardButton("Litecoin", callback_data="litecoin_tracks")
    dogecoin_button = InlineKeyboardButton("Dogecoin", callback_data="dogecoin_tracks")
    cardano_button = InlineKeyboardButton("Cardano", callback_data="cardano_tracks")

    keyboard = InlineKeyboardMarkup().add(
        bitcoin_button,
        ethereum_button,
        litecoin_button,
        dogecoin_button,
        cardano_button,
    )

    return keyboard
