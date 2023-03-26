import random

from aiogram import types, Dispatcher

from bot.send.higher import send_message_higher


def register_message_handler(dispatcher: Dispatcher):
    """
        Register handler for message
    :param dispatcher: aiogram dispatcher
    :return: None
    """
    dispatcher.register_message_handler(callback=test_command, commands=['test'])


async def test_command(message: types.Message) -> None:
    await send_message_higher(
        id_user=message.from_user.id, currency="BTC-USD", price_currency=random.randint(20000, 27000)
    )