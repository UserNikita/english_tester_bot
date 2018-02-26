import telebot
import settings
import random
from game import Game, ExpectedAnswerNotFoundException
from statistics import Statistics

bot = telebot.TeleBot(settings.TOKEN)


def send_question(user_id):
    """Функция для отправки вопроса пользователю с указанным user_id.
    Генерирует новый вопрос, добавляет клавиатуру для выбора ответа и отправляет это пользователю.
    :param user_id: int идентификатор пользователя
    """
    question_obj = Game(user_id=user_id).get_question_object()
    keyboard = generate_keyboard(
        right_answer=question_obj.right_answer,
        wrong_answers=question_obj.wrong_answers)
    question = '<b>%s</b>' % question_obj.question
    bot.send_message(user_id, question, reply_markup=keyboard, parse_mode='HTML')


def generate_keyboard(right_answer, wrong_answers):
    """Функция для генерации клавиатуры.
    Принимает варианты ответа перемешивает и возвращает в виде разметки клавиатуры для ответа
    :param right_answer: str правильный вариант ответа
    :param wrong_answers: list of str список неправильных вариантов ответа
    :return: объект класса telebot.types.ReplyKeyboardMarkup
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)

    answers = [right_answer]
    answers.extend(wrong_answers)
    random.shuffle(answers)

    keyboard.add(*answers)
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def start(message):
    """Обработчик команды /start и /help"""
    text = ("Я хочу сыграть с тобой в игру\n"
            "Правила просты. Я даю тебе перевод слова на русский язык, "
            "а тебе нужно выбрать его из предложенных вариантов.\n\n"
            "Основные команды:\n"
            "/game - начать игру\n"
            "/stop - завершить игру\n"
            "/stat - вывод статистики\n"
            "/help и /start - вывод помощи\n\n"
            "Чтобы начать вызови команду /game")
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['stop'])
def stop(message):
    """Обработчик команды /stop"""
    user_id = message.from_user.id
    Game(user_id=user_id).end_game()
    keyboard_remover = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Спасибо за честную игру", reply_markup=keyboard_remover)


@bot.message_handler(commands=['game'])
def game(message):
    """Обработчик команды /game"""
    send_question(user_id=message.from_user.id)


@bot.message_handler(commands=['stat'])
def statistic(message):
    """Обработчик команды /stat"""
    stat = Statistics(user_id=message.from_user.id)
    text = str(stat)
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    """Функция для получения ответов от пользователя и их проверки"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    keyboard_remover = telebot.types.ReplyKeyboardRemove()

    try:
        if Game(user_id=user_id).check_answer(message.text):
            Statistics(user_id=user_id).add_right_answer()
            bot.send_message(chat_id, "Правильно {}".format(settings.RIGHT_ANSWER_EMOJI),
                             reply_markup=keyboard_remover)
        else:
            Statistics(user_id=user_id).add_wrong_answer()
            bot.send_message(chat_id, "Неправильно {}".format(settings.WRONG_ANSWER_EMOJI),
                             reply_markup=keyboard_remover)
        send_question(user_id=user_id)
    except ExpectedAnswerNotFoundException:
        bot.send_message(chat_id, "Чтобы начать игру введи команду /game", reply_markup=keyboard_remover)


if __name__ == '__main__':
    bot.polling(none_stop=True)
