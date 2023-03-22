import env

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DataBase.storage import DataBaseManager
from src.blockchain import BlockChain

bot = Bot(token=env.TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
db = DataBaseManager("DataBase/database.db")
blockchain = BlockChain()
