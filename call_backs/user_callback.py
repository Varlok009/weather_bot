from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from data_base.BaseUserTg import BaseUserTg
from config import DATABASE
from weathers.cur_weather import get_cur_weather
import json


async def get_geo(callback: types.CallbackQuery):
    """Возвращает погоду в соответствии с нажатой инлайн кнопкой"""
    number_loc = int(callback.data[-1])
    db = BaseUserTg(DATABASE)
    # Извлекаем из БД и преобразуем json в кортеж словарей, выбираем нужный словарь в соотв. с калбеком
    geo = json.loads(db.get_user_location(callback.from_user.id)[number_loc])

    if 'user_id' in geo.keys():
        # await callback.message.answer(f"{geo}")
        await callback.message.answer(get_cur_weather(geo['lat'], geo['lon']))  # функция запроса погоды по гео данным
    else:
        await callback.message.answer('Нет сохраненной локации, используйте команду /добавить')

    await callback.answer()  # "Говорим", что калбэк отработал (снимает часы ожидания)


def register_callback_user(dp: Dispatcher):
    dp.register_callback_query_handler(get_geo, Text(startswith='get_loc'))
