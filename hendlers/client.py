import json
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.client_kb import keyboard_client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from weathers.cur_weather import get_cur_weather
from data_base.BaseUserTg import BaseUserTg
from config import DATABASE


async def get_start(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.send_message(message.from_user.id, 'Я бот который показывает погоду на основании гео данных',
                           reply_markup=keyboard_client)
    db = BaseUserTg(DATABASE)
    users = db.get_users_bot()
    if (message.from_user.id, ) not in users:
        db.add_user(message.from_user.id)


async def get_info(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.send_message(message.from_user.id, 'Список доступных команд:\n'
                                                 '/add_place - добавить/изменить данные локации')


async def get_current_geo(message: types.location):
    await bot.delete_message(message.from_user.id, message.message_id)
    # await bot.send_message(message.from_user.id, f'lon - {message.location.longitude}, '
    #                                              f'lat = {message.location.latitude}')
    await bot.send_message(message.from_user.id, get_cur_weather(message.location.latitude, message.location.longitude))


async def choice_save_geo(message: types.Message):
    # """""""
    await bot.delete_message(message.from_user.id, message.message_id)
    db = BaseUserTg(DATABASE)
    # Выгружает из БД кортеж json'ов, преобразует в список словарей
    locations = [json.loads(s) for s in db.get_user_location(message.from_user.id)]

    keyboard_save_location = InlineKeyboardMarkup()
    button_loc1 = InlineKeyboardButton(f"{locations[0]['name_location']}", callback_data="get_loc0")
    button_loc2 = InlineKeyboardButton(f"{locations[1]['name_location']}", callback_data="get_loc1")
    keyboard_save_location.row(button_loc1, button_loc2)

    await bot.send_message(message.from_user.id, 'Выберите сохраненную локацию', reply_markup=keyboard_save_location)
    # await bot.send_message(message.from_user.id, locations)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(get_start, commands=['start'])
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_message_handler(get_current_geo, content_types=['location'])
    dp.register_message_handler(choice_save_geo, commands=['Выбрать_из_сохраненных_локаций'])
