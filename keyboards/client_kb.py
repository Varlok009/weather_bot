from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
button_get_geo = KeyboardButton('Погода рядом со мной', request_location=True)
button_save_geo = KeyboardButton('/Выбрать_из_сохраненных_локаций')
keyboard_client.add(button_get_geo).insert(button_save_geo)

kb_exit = InlineKeyboardMarkup()
exit_but = InlineKeyboardButton(text='Отменить изменение локации', callback_data='exit')
kb_exit.add(exit_but)



