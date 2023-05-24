from aiogram import types, Dispatcher
from src.utils.loader import db


def register_message_handler(dispatcher: Dispatcher):
    """
        Register handler for message
    :param dispatcher: aiogram dispatcher
    :return: None
    """
    dispatcher.register_message_handler(callback=user_data, commands=['data'])


async def user_data(message: types.Message) -> None:
    user_data = db.get_user_data(message.from_user.id)
    print(user_data)
