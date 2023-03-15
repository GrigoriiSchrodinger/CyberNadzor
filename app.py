from aiogram import types
from aiogram.utils import executor
import settings
from loader import dp, db

logger = settings.setup_custom_logger('root')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    db.add_users(
        username=message.chat.username,
        last_name=message.chat.last_name,
        first_name=message.chat.first_name,
        id_user=message.chat.id
    )


async def on_startup(dp):
    db.create_tables()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
