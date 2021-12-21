from aiogram import Bot
from aiogram import Dispatcher
from config import TOKEN_TG
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#  Будем созранять данные о состоянии в оперативную память
storage = MemoryStorage()

bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot, storage=storage)