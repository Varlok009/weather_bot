from aiogram.utils import executor
from hendlers import client, add_geo, others
from call_backs import user_callback
from create_bot import dp
from config import DATABASE
from data_base.BaseUserTg import BaseUserTg


async def on_startup(_):
    db = BaseUserTg(DATABASE)
    db.create_db()
    print('Бот запущен')


client.register_handlers_client(dp)
add_geo.register_handlers_add_location(dp)
user_callback.register_callback_user(dp)
others.register_handlers_others(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
