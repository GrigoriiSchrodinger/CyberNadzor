from aiogram import Bot, Dispatcher

import env
from DataBase.storage import DataBaseManager


bot = Bot(token=env.TOKEN)
dp = Dispatcher(bot)
db = DataBaseManager("DataBase/database.db")
