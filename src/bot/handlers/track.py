import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from asset.dialogues import (
    tracks_dialog, indicate_price, specify_currency_track,
    only_numbers, again, notification_alert_below, notification_alert_higher
)
from src.bot.keyboards.inline.currency import keyboard_tracks
from src.bot.keyboards.inline.tracks_inline import keyboard_traces
from src.loader import db, bot
from src.number_formatting import formatting
from src.bot.states.tracks import Tracks

# KEYBOARDS
keyboard_traces: InlineKeyboardMarkup = keyboard_traces()
keyboard_tracks: InlineKeyboardMarkup = keyboard_tracks()


def is_number(number) -> bool:
    pattern = r'^\d*([\.,]\d+)?$'
    return bool(re.match(pattern, number))


def register_message_handler(dispatcher: Dispatcher) -> None:
    """
        Register handler for message
    :param dispatcher: aiogram dispatcher
    :return: None
    """
    dispatcher.register_message_handler(callback=track_command, commands=['track'])
    dispatcher.register_message_handler(callback=set_currency, state=Tracks.VALUE)


def register_callback_query_handler(dispatcher: Dispatcher) -> None:
    """
        Регистрация обработчика для callback query
    :param dispatcher: aiogram dispatcher
    :return: None
    """
    dispatcher.register_callback_query_handler(callback=send_track_bitcoin, text="bitcoin_tracks")
    dispatcher.register_callback_query_handler(callback=send_track_ethereum, text="ethereum_tracks")
    dispatcher.register_callback_query_handler(callback=send_track_litecoin, text="litecoin_tracks")
    dispatcher.register_callback_query_handler(callback=send_track_dogecoin, text="dogecoin_tracks")
    dispatcher.register_callback_query_handler(callback=send_track_cardano, text="cardano_tracks")
    dispatcher.register_callback_query_handler(callback=send_below, text="below")
    dispatcher.register_callback_query_handler(callback=send_higher, text="higher")


async def track_command(message: types.Message) -> None:
    await message.answer(text=specify_currency_track, reply_markup=keyboard_tracks)


async def send_track_bitcoin(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text=tracks_dialog.format(currency="bitcoin"), reply_markup=keyboard_traces)
    await state.update_data(currency="BTC-USD")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_track_ethereum(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text=tracks_dialog.format(currency="ethereum"), reply_markup=keyboard_traces)
    await state.update_data(currency="ETH-USD")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_track_litecoin(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text=tracks_dialog.format(currency="litecoin"), reply_markup=keyboard_traces)
    await state.update_data(currency="LTC-USD")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_track_dogecoin(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text=tracks_dialog.format(currency="dogecoin"), reply_markup=keyboard_traces)
    await state.update_data(currency="DOGE-USD")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_track_cardano(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text=tracks_dialog.format(currency="cardano"), reply_markup=keyboard_traces)
    await state.update_data(currency="ADA-USD")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_below(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(track="below")
    await Tracks.VALUE.set()
    await call.message.answer(indicate_price)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_higher(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(track="higher")
    await Tracks.VALUE.set()
    await call.message.answer(indicate_price)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def set_currency(message: types.Message, state: FSMContext) -> None:
    data: dict = await state.get_data()
    currency: str = data['currency']
    table: str = data['track']
    quantity: str = message.text
    id_user: str = message.from_user.id

    if is_number(quantity):
        if table == "below":
            db.update_currency(
                table="below_track",
                currency=currency,
                quantity=float(quantity.replace(',', '')),
                id_user=id_user
            )
            await bot.send_message(
                id_user, notification_alert_below.format(currency=currency, quantity=formatting(quantity))
            )

        elif table == "higher":
            db.update_currency(
                table="higher_track",
                currency=currency,
                quantity=float(quantity.replace(',', '')),
                id_user=id_user
            )
            await bot.send_message(
                id_user, notification_alert_higher.format(currency=currency, quantity=formatting(quantity))
            )
    else:
        await bot.send_message(
            message.from_user.id, only_numbers
        )
        await bot.send_message(
            message.from_user.id, again
        )
    await state.finish()