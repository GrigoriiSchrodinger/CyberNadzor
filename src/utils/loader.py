import src.env

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.blockchain import BlockChainPrice
from src.database.storage import DataBaseManager

bot = Bot(token=src.env.TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
blockchain = BlockChainPrice()
db = DataBaseManager("src/database/database.db")
