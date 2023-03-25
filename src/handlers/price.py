from aiogram import types, Dispatcher
from asset.dialogues import price_dialog, specify_currency_price
from src.keyboards.inline.currency import keyboard_price
from loader import blockchain, bot


def register_message_handler(dispatcher: Dispatcher):
    """
        Register handler for message
    :param dispatcher: aiogram dispatcher
    :return: None
    """
    dispatcher.register_message_handler(callback=price_command, commands=['price'])


def register_callback_query_handler(dispatcher: Dispatcher) -> None:
    """
        Регистрация обработчика для callback query
    :param dispatcher: aiogram dispatcher
    :return: None
    """
    dispatcher.register_callback_query_handler(callback=send_price_bitcoin, text="bitcoin_price")
    dispatcher.register_callback_query_handler(callback=send_price_ethereum, text="ethereum_price")
    dispatcher.register_callback_query_handler(callback=send_price_litecoin, text="litecoin_price")
    dispatcher.register_callback_query_handler(callback=send_price_dogecoin, text="dogecoin_price")
    dispatcher.register_callback_query_handler(callback=send_price_cardano, text="cardano_price")


async def price_command(message: types.Message) -> None:
    await message.answer(text=specify_currency_price, reply_markup=keyboard_price())


async def send_price_bitcoin(call: types.CallbackQuery) -> None:
    await call.message.answer(text=price_dialog.format(currency="Bitcoin", price=blockchain.price_bitcoin()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_price_ethereum(call: types.CallbackQuery) -> None:
    await call.message.answer(text=price_dialog.format(currency="Ethereum", price=blockchain.price_ethereum()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_price_litecoin(call: types.CallbackQuery) -> None:
    await call.message.answer(text=price_dialog.format(currency="Litecoin", price=blockchain.price_litecoin()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_price_dogecoin(call: types.CallbackQuery) -> None:
    await call.message.answer(text=price_dialog.format(currency="Dogecoin", price=blockchain.price_dogecoin()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_price_cardano(call: types.CallbackQuery) -> None:
    await call.message.answer(text=price_dialog.format(currency="Dogecoin", price=blockchain.price_cardano()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
