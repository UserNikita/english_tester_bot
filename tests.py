import unittest
from game import Game, ExpectedAnswerNotFoundException
from statistics import Statistics


class GameTestCase(unittest.TestCase):
    user_id = 0

    def test_right_answer(self):
        """Проверка правильности работы при правильном ответе пользователя"""
        # Получаем вопрос
        question_object = Game(user_id=self.user_id).get_question_object()
        # Даём правильный ответ
        self.assertTrue(Game(user_id=self.user_id).check_answer(question_object.right_answer))
        # Завершаем игру
        Game(user_id=self.user_id).end_game()
        # Убеждаемся, что от пользователя не ожидается ответ
        self.assertRaises(ExpectedAnswerNotFoundException, lambda: Game(user_id=self.user_id).check_answer('answer'))

    def test_wrong_answer(self):
        """Проверка правильности работы при неправильном ответе пользователя"""
        # Получаем вопрос
        question_object = Game(user_id=self.user_id).get_question_object()
        # Создаём неправильный ответ
        wrong_answer = 'wrong '+question_object.right_answer
        # Даём неправильный ответ
        self.assertFalse(Game(user_id=self.user_id).check_answer(wrong_answer))
        # Завершаем игру
        Game(user_id=self.user_id).end_game()
        # Убеждаемся, что от пользователя не ожидается ответ
        self.assertRaises(ExpectedAnswerNotFoundException, lambda: Game(user_id=self.user_id).check_answer('answer'))

    def tearDown(self):
        """Правильное завершение игры для пользователя"""
        Game(user_id=self.user_id).end_game()


class StatisticsTestCase(unittest.TestCase):
    user_id = 0

    def test_add_right_answer(self):
        """Проверка правильности работы статистики при добавлении верного ответа"""
        # Получаем текущие значения количества верных и неверных ответов
        old_right_answers_count = Statistics(user_id=self.user_id).get_right_answers_count()
        old_wrong_answers_count = Statistics(user_id=self.user_id).get_wrong_answers_count()

        # Добавление в статистику правильного ответа
        Statistics(user_id=self.user_id).add_right_answer()

        # Получение новых значений количества верных и неверных ответов
        new_right_answers_count = Statistics(user_id=self.user_id).get_right_answers_count()
        new_wrong_answers_count = Statistics(user_id=self.user_id).get_wrong_answers_count()

        # Количество верных ответов должно увеличиться на 1
        self.assertEqual(old_right_answers_count+1, new_right_answers_count)
        # Количество неверных ответов должно остаться неизменным
        self.assertEqual(old_wrong_answers_count, new_wrong_answers_count)

    def test_add_wrong_answer(self):
        """Проверка правильности работы статистики при добавлении неверного ответа"""
        # Получаем текущие значения количества верных и неверных ответов
        old_right_answers_count = Statistics(user_id=self.user_id).get_right_answers_count()
        old_wrong_answers_count = Statistics(user_id=self.user_id).get_wrong_answers_count()

        # Добавление в статистику неправильного ответа
        Statistics(user_id=self.user_id).add_wrong_answer()

        # Получение новых значений количества верных и неверных ответов
        new_right_answers_count = Statistics(user_id=self.user_id).get_right_answers_count()
        new_wrong_answers_count = Statistics(user_id=self.user_id).get_wrong_answers_count()

        # Количество верных ответов должно увеличиться на 1
        self.assertEqual(old_right_answers_count, new_right_answers_count)
        # Количество неверных ответов должно остаться неизменным
        self.assertEqual(old_wrong_answers_count+1, new_wrong_answers_count)

    def tearDown(self):
        """Очищаем статистику для данного пользователя"""
        Statistics(user_id=self.user_id).clear()


if __name__ == '__main__':
    unittest.main()
