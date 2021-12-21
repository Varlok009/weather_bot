from aiogram import Dispatcher, types
from create_bot import bot


async def bla_bla(message: types.Message):
    await bot.send_message(message.from_user.id, 'Мой ленивый создатель не придумал, что я могу на это ответить :(. '
                                                 'Вы можете посмотреть список доступных команд, отправив /info')


def register_handlers_others(dp: Dispatcher):
    dp.register_message_handler(bla_bla)