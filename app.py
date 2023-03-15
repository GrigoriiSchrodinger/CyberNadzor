from aiogram import types
from aiogram.utils import executor
import settings
from loader import dp, db

logger = settings.setup_custom_logger('root')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    print("xyu")


async def on_startup(dp):
    logger.debug('main message')
    db.create_tables()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
