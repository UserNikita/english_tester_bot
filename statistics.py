import shelve
import settings


class Statistics:
    """Класс предназначенный для сохранения количества правильных и неправильных ответов пользователя"""

    def __init__(self, user_id):
        """ Метод для инициализации объекта статистики
        :param user_id: Идентификатор пользователя
        """
        self.user_id = str(user_id)

    def __str__(self):
        right_count, wrong_count = self._get_answers_count()
        all_count = right_count + wrong_count

        if all_count == 0:  # Нет ни одного ответа
            s = "Правильных ответов: {}\n" \
                "Неправильных ответов: {}\n" \
                "Всего ответов: {}" \
                .format(right_count, wrong_count, all_count)
        else:
            right_count_percent = (100 / all_count) * right_count
            wrong_count_percent = 100 - right_count_percent
            s = "Правильных ответов: {} ({:.2f}%)\n" \
                "Неправильных ответов: {} ({:.2f}%)\n" \
                "Всего ответов: {}" \
                .format(right_count, right_count_percent, wrong_count, wrong_count_percent, all_count)
        return s

    def _get_answers_count(self):
        """Метод для получения счётчиков правильных и неправильных ответов из файла
        :return: Список вида [X, Y], где X - количество правильных ответов, а Y - количество неправильных
        """
        with shelve.open(settings.STATISTICS_SHELVE_NAME) as storage:
            return storage[self.user_id] if self.user_id in storage else [0, 0]

    def _write_answers_count(self, counter):
        """Метод для записи счётчиков правильных и неправильных ответов в файл
        :param counter: Список вида [X, Y], где X - количество правильных ответов, а Y - количество неправильных
        """
        with shelve.open(settings.STATISTICS_SHELVE_NAME) as storage:
            storage[self.user_id] = counter

    def clear(self):
        """Метод для очистки статистики"""
        with shelve.open(settings.STATISTICS_SHELVE_NAME) as storage:
            if self.user_id in storage:
                del storage[self.user_id]

    def get_right_answers_count(self):
        """Метод для получения количества правильных ответов"""
        return self._get_answers_count()[0]

    def get_wrong_answers_count(self):
        """Метод для получения количества неправильных ответов"""
        return self._get_answers_count()[1]

    def add_right_answer(self):
        """Метод для увеличения счётчика правильных ответов на 1"""
        counter = self._get_answers_count()
        counter[0] += 1
        self._write_answers_count(counter=counter)

    def add_wrong_answer(self):
        """Метод для увеличения счётчика неправильных ответов на 1"""
        counter = self._get_answers_count()
        counter[1] += 1
        self._write_answers_count(counter=counter)
