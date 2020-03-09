import mysql.connector
from mysql.connector import errorcode

from flask import g

import config


class DB:
    def __init__(self):
        self._connect = self._connect_mysql()
        if self._connect is not None:
            self._cursor = self._connect.cursor()
            self._init_db()
    

    def _connect_mysql(self):
        # соединение с сервером MySQL
        try:
            cnx = mysql.connector.connect(**config.CONFIG_DATABASE)
        except mysql.connector.Error as err:
            return None
        return cnx


    def _init_db(self):
        try:
            # self._cursor.execute("USE %s", (config.DATABASE, ))  # !!! ERROR 1064(42000): ИМЯ БД ПЕРЕДАЕТСЯ С КАВЫЧКАМИ????
            self._cursor.execute(f"USE {config.DATABASE}")
        except mysql.connector.Error as err:
            with open('schema.sql', 'rt') as schema:
                self._cursor.execute(schema.read(), multi=True)
    

    def close(self):
        self._connect.close()

    def add_new_user(self, user_data):
        """
        Добавление нового пользователя в базу данных
        user_data - кортеж с данными о пользователе
        (имя, фамилия, email, пол, дата рождения)
        Возвращает id нового пользователя
        """

        query = """
                INSERT INTO users 
                (first_name, last_name, email, gender, birsday)
                VALUES (%s, %s, %s, %s, %s);
                """
        self._cursor.execute(query, user_data)
        
        self._cursor.execute('SELECT LAST_INSERT_ID();')
        id = self._cursor.fetchone()[0]
        
        self._connect.commit()
        return id


    def add_new_feedback(self, feedback_data, user_id):
        """
        Добавление нового отзыва в базу данных
        feedback_data - кортеж с данными о пользователе
        (имя, email, текст сообщения)
        """

        query = """
                INSERT INTO feedback 
                (name, email, message)
                VALUES (%s, %s, %s);
                """
        self._cursor.execute(query, feedback_data)

        self._cursor.execute('SELECT LAST_INSERT_ID();')
        id = self._cursor.fetchone()[0]
        self._connect.commit()

        self._add_relations(user_id, id)


    def _add_relations(self, user_id, feedback_id):
        """Добавление новой связи пользователь-сообщение"""
        query = """
                INSERT INTO user_feedback 
                (user_id, feedback_id)
                VALUES (%s, %s);
                """
        self._cursor.execute(query, (user_id, feedback_id))
        self._connect.commit()


    def is_exist_email(self, email):
        """
        Функция проверяет наличие введенного email в БД
        """
        self._cursor.execute("SELECT id FROM users WHERE email=%s", (email, ))
        return self._cursor.fetchone() is not None

    def get_data_user(self, email):
        """Возвращает кортеж с данными зарегистрированного пользователя"""
        query = "SELECT * FROM users WHERE email=%s"
        self._cursor.execute(query, (email, ))
        return self._cursor.fetchone()


    def get_list_feedback(self):
        query = "SELECT id, name, message FROM feedback ORDER BY id DESC LIMIT 10"
        self._cursor.execute(query)
        return self._cursor.fetchall()

    
    def test_db(self):
        char = 'U%'
        self._cursor.execute('SHOW TABLES')
        for tables in self._cursor:
            print(tables[0])

    
def get_db():
    if "db" not in g:
        g.db = DB()
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    db = DB()
    db.test_db()


