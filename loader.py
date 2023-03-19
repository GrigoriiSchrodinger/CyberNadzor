from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import env
from DataBase.storage import DataBaseManager
from src.blockchain import BlockChain

bot = Bot(token=env.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DataBaseManager("DataBase/database.db")
blockchain = BlockChain()
