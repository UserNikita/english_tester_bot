import shelve
import settings
import database


class ExpectedAnswerNotFoundException(Exception):
    pass


class Question:
    """Класс вопроса. Гарантирует правильность заполнения всех полей"""
    def __init__(self, question, right_answer, wrong_answers):
        """Метод инициализации объекта вопроса
        :param question: str вопрос
        :param right_answer: str правильный ответ
        :param wrong_answers: list of str список неправильных ответов
        """
        assert isinstance(question, str), "'question' is not a string"
        assert isinstance(right_answer, str), "'right_answer' is not a string"
        assert isinstance(wrong_answers, list), "'wrong_answers' is not a list"
        self.question = question
        self.right_answer = right_answer
        self.wrong_answers = wrong_answers


class Game:
    def __init__(self, user_id):
        """Метод для инициализации объекта игры
        :param user_id: идентификатор пользователя
        """
        self.user_id = str(user_id)

    @property
    def expected_answer(self):
        with shelve.open(settings.SHELVE_NAME) as storage:
            try:
                return storage[self.user_id]
            except KeyError:
                return None

    @expected_answer.setter
    def expected_answer(self, value):
        with shelve.open(settings.SHELVE_NAME) as storage:
            storage[self.user_id] = value

    @expected_answer.deleter
    def expected_answer(self):
        with shelve.open(settings.SHELVE_NAME) as storage:
            if self.user_id in storage.keys():
                del storage[self.user_id]

    def get_question_object(self):
        """Метод для получения вопроса с вариантами ответов
        :return: object в котором есть свойства: вопрос (question), правильный ответ (right_answer) и
        список неправильных ответов (wrong_answers)
        """
        db = database.DataBase(database_name=settings.DATABASE_NAME)

        random_word = db.get_random_word()
        question = random_word['translate']
        right_answer = random_word['word']

        wrong_answers = [db.get_random_word()['word'] for _ in range(3)]

        self.expected_answer = right_answer  # Этот ответ мы ожидаем получить от пользователя

        return Question(
            question=question,
            right_answer=right_answer,
            wrong_answers=wrong_answers
        )

    def check_answer(self, answer):
        """Метод для проверки правильности ответа
        :param answer: ответ пользователя
        :return: bool. True - если ответ верный, и False - если неверный.
        """
        if self.expected_answer is None:  # Никакой ответ от пользователя не ожидался
            raise ExpectedAnswerNotFoundException()

        if answer == self.expected_answer:
            return True
        return False

    def end_game(self):
        """Метод для завершения игры"""
        del self.expected_answer  # Больше не ожидаем ответа от пользователя
