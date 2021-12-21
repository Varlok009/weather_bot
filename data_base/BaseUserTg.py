import sqlite3
import json


class BaseUserTg:

    def __init__(self, db_file):
        #  Подключаеся к БД
        self.connection = sqlite3.connect(db_file)
        #  Сохраняем курсор
        self.cursor = self.connection.cursor()

    def get_users_bot(self):
        """Возвращает всех юзеров (id) бота"""
        with self.connection:
            return self.cursor.execute("Select id_user_tg From users").fetchall()

    def add_user(self, user_id):
        """Добавляет нового пользователя в БД"""
        self.cursor.execute(f"Insert Into users Values(?, ?, ?)",
                            (user_id, json.dumps({'name_location': 'пусто'}), json.dumps({'name_location': 'пусто'})))
        self.connection.commit()
        self.connection.close()

    def add_user_place(self, data):
        """Добавляет для пользователя новое место"""
        if (data['user_id'],) not in self.get_users_bot():  # в таком случае соединение закроется и все сломается
            self.add_user(data['user_id'])

        place = data['loc_number']
        del data['loc_number']
        self.cursor.execute(f"Update users Set {place} == ? Where id_user_tg == ?", (json.dumps(data), data['user_id']))
        self.connection.commit()
        self.connection.close()

    def get_user_location(self, user_id, place=None):
        """Возвращает данные локации по номеру user id"""
        if not place:
            return self.cursor.execute("Select place1, place2 From users Where id_user_tg == ?", (user_id,)).fetchone()
        # else:
        #     place = 'place' + str(place + 1)
        #     return self.cursor.execute("Select ? From users Where id_user_tg == ?", (place, user_id)).fetchone()

    def create_db(self):
        """Создает таблицы на основании скрипта"""
        with open('data_base/sq_db.sql', mode='r') as f:
            self.cursor.executescript(f.read())
        self.connection.commit()
        self.connection.close()


    # def close_db(self):
    #     """закрывает соединение с БД"""
    #     self.connection.close()