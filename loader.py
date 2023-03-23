import env

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.storage import DataBaseManager
from src.blockchain import BlockChainPrice

bot = Bot(token=env.TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
blockchain = BlockChainPrice()
db = DataBaseManager("database/database.db")
