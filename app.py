from aiogram import types
from aiogram.utils import executor
import settings
from asset.dialogues import start_dialog_not_registered, start_dialog_is_registered
from asset.text_logo import logo
from loader import dp, db

logger = settings.setup_custom_logger('root')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if db.check_user(message.chat.id) is None:
        db.add_user(
            username=message.chat.username,
            last_name=message.chat.last_name,
            first_name=message.chat.first_name,
            id_user=message.chat.id
        )
        await message.answer(start_dialog_not_registered.format(name=message.chat.first_name))
    else:
        await message.answer(start_dialog_is_registered.format(name=message.chat.first_name))


async def on_startup(dp):
    db.create_tables()


if __name__ == "__main__":
    logger.info(logo)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
