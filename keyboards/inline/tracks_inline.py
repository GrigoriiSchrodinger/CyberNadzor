from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_traces():
    below_button = InlineKeyboardButton("Ниже", callback_data="below")
    higher_button = InlineKeyboardButton("Выше", callback_data="higher")

    keyboard = InlineKeyboardMarkup().add(
        below_button,
        higher_button,
    )

    return keyboard
