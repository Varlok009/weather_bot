from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from data_base.BaseUserTg import BaseUserTg
from config import DATABASE
from weathers.cur_weather import get_cur_weather
import json


async def get_geo(callback: types.CallbackQuery):
    """Возвращает погоду в соответствии со сработавшим колбеком от нажатия на инлайн кнопку"""

    number_loc = int(callback.data[-1])
    db = BaseUserTg(DATABASE)
    # Извлекае из БД и преобразуем json в кортеж словарей, выбираем нужный словарь в соотв. с калбеком
    geo = json.loads(db.get_user_location(callback.from_user.id)[number_loc])

    await callback.message.answer(get_cur_weather(geo['lat'], geo['lon']))  # функция запроса погоды по гео данным
    await callback.answer()  # "Говорим", что калбэк отработал (снимает часы ожидания)


async def catch_empty_location(callback: types.CallbackQuery):
    """Выводит подсказку пользователю, если тот пытается получить погоду по пустой ячейке"""

    await callback.message.answer("Данные о локации не сохранены, сначала используйте команду /add_place")


def register_callback_user(dp: Dispatcher):
    dp.register_callback_query_handler(get_geo, Text(startswith="get_loc"))
    dp.register_callback_query_handler(catch_empty_location, Text(startswith="none_loc"))
