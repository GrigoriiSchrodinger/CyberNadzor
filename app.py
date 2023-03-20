# import asyncio
from aiogram.dispatcher import FSMContext

import settings

from aiogram import types
from aiogram.utils import executor
from asset.dialogues import start_dialog_not_registered, start_dialog_is_registered, price_dialog, help_dialog, \
    tracks_dialog
from asset.text_logo import logo
from keyboards.inline.currency import keyboard_price, keyboard_tracks
from keyboards.inline.tracks_inline import keyboard_traces
from loader import dp, db, blockchain, bot
from states.tracks import Tracks

# from src.blockchain import BlockChain

logger = settings.setup_custom_logger('root')


@dp.message_handler(commands=['start'])
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


@dp.message_handler(commands=['price'])
async def price_command(message: types.Message):
    await message.answer(text="Пожалуйста, уточните, какую валюту вы желаете увидеть", reply_markup=keyboard_price())


@dp.message_handler(commands=['track'])
async def track_command(message: types.Message):
    if db.check_user(message.chat.id, "users") is None:
        db.add_user(
            username=message.chat.username,
            last_name=message.chat.last_name,
            first_name=message.chat.first_name,
            id_user=message.chat.id
        )
    await message.answer(text="За какой валютой начать следить?", reply_markup=keyboard_tracks())


@dp.message_handler(commands=['help'])
async def price_command(message: types.Message):
    await message.answer(text=help_dialog)


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------Price handler---------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="bitcoin_price")
async def send_price_bitcoin(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Bitcoin", price=blockchain.price_bitcoin()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="ethereum_price")
async def send_price_ethereum(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Ethereum", price=blockchain.price_ethereum()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="litecoin_price")
async def send_price_litecoin(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Litecoin", price=blockchain.price_litecoin()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="dogecoin_price")
async def send_price_dogecoin(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Dogecoin", price=blockchain.price_dogecoin()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="cardano_price")
async def send_price_dogecoin(call: types.CallbackQuery):
    await call.message.answer(text=price_dialog.format(currency="Dogecoin", price=blockchain.price_cardano()))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------Track handler---------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="bitcoin_tracks")
async def send_track_bitcoin(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text=tracks_dialog.format(currency="bitcoin"), reply_markup=keyboard_traces())
    await state.update_data(currency="bitcoin")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="ethereum_tracks")
async def send_track_ethereum(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text=tracks_dialog.format(currency="ethereum"), reply_markup=keyboard_traces())
    await state.update_data(currency="ethereum")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="litecoin_tracks")
async def send_track_litecoin(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text=tracks_dialog.format(currency="litecoin"), reply_markup=keyboard_traces())
    await state.update_data(currency="litecoin")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="dogecoin_tracks")
async def send_track_dogecoin(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text=tracks_dialog.format(currency="dogecoin"), reply_markup=keyboard_traces())
    await state.update_data(currency="dogecoin")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="cardano_tracks")
async def send_track_dogecoin(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text=tracks_dialog.format(currency="cardano"), reply_markup=keyboard_traces())
    await state.update_data(currency="cardano")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="below")
async def send_below(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(track="below")
    await Tracks.VALUE.set()
    await call.message.answer("Напиши при какой цене нужно будет сообщить:")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="higher")
async def send_below(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(track="higher")
    await Tracks.VALUE.set()
    await call.message.answer("Напиши при какой цене нужно будет сообщить:")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def is_number(stroka: str):
    try:
        float(stroka)
        return True
    except ValueError:
        return False


@dp.message_handler(state=Tracks.VALUE)
async def process_next_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if is_number(message.text):
        if data['track'] == "below":
            currency: str = data['currency']
            if db.check_user(message.from_user.id, "below_track") is None:
                db.request(
                    f"INSERT INTO below_track (id_users, '{currency}') VALUES ('{message.from_user.id}', '{message.text}')")
            else:
                db.request(
                    f"UPDATE below_track SET '{currency}'='{message.text}' WHERE id_users='{message.from_user.id}'")

            await bot.send_message(
                message.from_user.id, f"Хорошо, я сообщу тебе когда {currency} будет ниже {message.text}"
            )

        elif data['track'] == "higher":
            currency: str = data['currency']
            if db.check_user(message.from_user.id, "higher_track") is None:
                db.request(
                    f"INSERT INTO higher_track (id_users, '{currency}') VALUES ('{message.from_user.id}', '{message.text}')")
            else:
                db.request(
                    f"UPDATE higher_track SET '{currency}'='{message.text}' WHERE id_users='{message.from_user.id}'")

            await bot.send_message(
                message.from_user.id, f"Хорошо, я сообщу тебе когда {data['currency']} будет выше {message.text}"
            )
    else:
        await bot.send_message(
            message.from_user.id, f"Но это же не число, попробуй еще раз"
        )
    await state.finish()


async def on_startup(dp):
    db.create_tables()
    # asyncio.create_task(BlockChain().check())


if __name__ == "__main__":
    logger.info(logo)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
