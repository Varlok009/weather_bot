from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from data_base.BaseUserTg import BaseUserTg
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DATABASE
from create_bot import dp, bot
from keyboards.client_kb import kb_exit
from weathers.lon_validator import lon_validator
from weathers.lat_validator import lat_validator
import json


class AddGeo(StatesGroup):
    """Класс содержащий состояния, необходимые для добавления и сохранения геолокаций"""

    loc_number = State()
    name_location = State()
    lat = State()
    lot = State()


async def choice_location(message: types.Message):
    """Выгружает из БД текущие сохраненные данные локаций. Добавляет их в иноайн клавиатуру."""

    await bot.delete_message(message.from_user.id, message.message_id)
    db = BaseUserTg(DATABASE)

    # Выгружает из БД кортеж c геоданными локаций, преобразует в список словарей, если геоднанные присутсвуют
    locations = db.get_user_location(message.from_user.id)
    locations = [json.loads(s) if s else None for s in locations]

    # Создает инлайн клавиатуру и кнопки из всех полученных геоданных
    keyboard_save_location = InlineKeyboardMarkup()
    buttons_loc = [InlineKeyboardButton(f"{loc['name_location']}", callback_data=f"save_loc{ind}") if loc
                   else InlineKeyboardButton("пусто", callback_data=f"save_loc{ind}")
                   for ind, loc in enumerate(locations)]
    keyboard_save_location.row(*buttons_loc)

    await bot.send_message(message.from_user.id, 'Выберите ячеку, которую хотите изменить',
                           reply_markup=keyboard_save_location)


async def start_add_geo(callback: types.CallbackQuery, state=None):
    """Запускает машину состояний"""

    await AddGeo.loc_number.set()
    async with state.proxy() as data:
        data['loc_number'] = f"place{str(int(callback.data[-1]) + 1)}"

    await AddGeo.next()
    await bot.send_message(callback.from_user.id, 'Напиши название локации', reply_markup=kb_exit)


async def cancel_state(callback: types.CallbackQuery, state=FSMContext):
    """Выводит из состояния"""

    current_state = await state.get_state()
    if not current_state:
        return
    await state.finish()
    await bot.send_message(callback.from_user.id, 'Процесс изменения ячейки прерван пользователем')


async def save_name_location(message: types.Message, state=FSMContext):
    """Сохраняет название локации и id пользователя в словарь"""

    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['name_location'] = message.text
    await AddGeo.next()
    await message.reply('Теперь введи значение широты', reply_markup=kb_exit)


async def save_lat_location(message: types.Message, state=FSMContext):
    """Сохраняет значение широты локации в словарь, если оно прошло валидацию"""

    if not lat_validator(message.text):
        await message.reply('Значение широты введено неверно, значение должно быть в интервале от -90 до 90, '
                            'в качестве разделителя необходимо использовать символ точки ".". Попробуйте еще раз.')
    else:
        async with state.proxy() as data:
            data['lat'] = message.text
            await AddGeo.next()
        await message.reply('Теперь введи значение долготы', reply_markup=kb_exit)


async def save_lon_location(message: types.Message, state=FSMContext):
    """Сохраняет значение долготы локации в словарь, если оно прошло валидацию.
    Отправляет результирующий словарь на запись в БД"""

    if not lon_validator(message.text):
        await message.reply('Значение долготы введено неверно, значение должно быть в интервале от -180 до 180, '
                            'в качестве разделителя необходимо использовать символ точки "."ю Попробуйте еще раз.')
    else:
        async with state.proxy() as data:
            data['lon'] = message.text
        db = BaseUserTg(DATABASE)
        async with state.proxy() as data:
            data_dict = dict(zip(data.keys(), data.values()))

            db.add_user_place(data_dict)
            await bot.send_message(message.from_user.id, f'Поздравляем, новая локация с именем '
                                                             f'{data["name_location"]} сохранена!')

        await state.finish()


def register_handlers_add_location(dp: Dispatcher):
    dp.register_message_handler(choice_location, commands='add_place', state=None)
    dp.register_callback_query_handler(start_add_geo, Text(startswith='save_loc'))
    dp.register_callback_query_handler(cancel_state, Text(startswith='exit'), state="*")
    dp.register_message_handler(cancel_state, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(save_name_location, content_types=['text'], state=AddGeo.name_location)
    dp.register_message_handler(save_lat_location, content_types=['text'], state=AddGeo.lat)
    dp.register_message_handler(save_lon_location, content_types=['text'], state=AddGeo.lot)
