import asyncio
import settings

from aiogram import types, Dispatcher
from aiogram.utils import executor
from asset.dialogues import (
    start_dialog_not_registered,
    start_dialog_is_registered,
    help_dialog
)
from asset.text_logo import logo
from src.loader import dispatcher, db
from bot.handlers import track, price, test_alert
from src.blockchain import RaceTrack


logger = settings.setup_custom_logger('root')


@dispatcher.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if db.check_user(message.chat.id, "users") is None:
        db.add_user(
            username=message.chat.username,
            last_name=message.chat.last_name,
            first_name=message.chat.first_name,
            id_user=message.chat.id
        )
        await message.answer(start_dialog_not_registered.format(name=message.chat.first_name))
    else:
        await message.answer(start_dialog_is_registered.format(name=message.chat.first_name))


@dispatcher.message_handler(commands=['help'])
async def price_command(message: types.Message):
    await message.answer(text=help_dialog)


async def on_startup(dispatcher: Dispatcher):
    db.create_tables()

    price.register_message_handler(dispatcher)
    price.register_callback_query_handler(dispatcher)

    track.register_message_handler(dispatcher)
    track.register_callback_query_handler(dispatcher)

    test_alert.register_message_handler(dispatcher)

    asyncio.create_task(RaceTrack().track_crypto())


if __name__ == "__main__":
    logger.info(logo)
    executor.start_polling(dispatcher, on_startup=on_startup, skip_updates=False)
