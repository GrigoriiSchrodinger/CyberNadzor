# import asyncio
import settings

from aiogram import types
from aiogram.utils import executor
from asset.dialogues import start_dialog_not_registered, start_dialog_is_registered, price_dialog, help_dialog
from asset.text_logo import logo
from keyboards.inline.currency import keyboard
from loader import dp, db, blockchain, bot

# from src.blockchain import BlockChain

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


@dp.message_handler(commands=['price'])
async def price_command(message: types.Message):
    await message.answer(text="Пожалуйста, уточните, какую валюту вы желаете увидеть", reply_markup=keyboard())


@dp.message_handler(commands=['help'])
async def price_command(message: types.Message):
    await message.answer(text=help_dialog)


@dp.callback_query_handler(text="bitcoin_data")
async def send_price_bitcoin(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Bitcoin", price=blockchain.price_bitcoin()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="ethereum_data")
async def send_price_ethereum(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Ethereum", price=blockchain.price_ethereum()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="litecoin_data")
async def send_price_litecoin(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Litecoin", price=blockchain.price_litecoin()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="dogecoin_data")
async def send_price_dogecoin(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Dogecoin", price=blockchain.price_dogecoin()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="cardano_data")
async def send_price_dogecoin(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Cardano", price=blockchain.price_cardano()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def on_startup(dp):
    db.create_tables()
    # asyncio.create_task(BlockChain().check())


if __name__ == "__main__":
    logger.info(logo)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
