import sqlite3
import random


class DataBase:
    """Класс для работы с базой данных"""

    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self._count_rows = None

    def get_random_word(self):
        """Метод для получения одной случайной записи из базы данных
        :return: dict - вида с ключами word (слово на английском языке) и translate (перевод данного слова)
        """
        sql_query = "SELECT * FROM `translate` WHERE id = ?"
        entry_id = random.randrange(1, self.count_rows()+1)
        entry = self.cursor.execute(sql_query, (entry_id,)).fetchall()[0]
        return {'word': entry[1], 'translate': entry[2]}

    def count_rows(self):
        """Метод для получения количества строк в базе данных
        :return: int - количество строк в базе данных
        """
        if not self._count_rows:
            sql_query = "SELECT COUNT(*) FROM `translate`"
            self._count_rows = self.cursor.execute(sql_query).fetchall()[0][0]
        return self._count_rows
