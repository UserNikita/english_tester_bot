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
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)

    answers = [right_answer]
    answers.extend(wrong_answers)
    random.shuffle(answers)

    buttons = [telebot.types.InlineKeyboardButton(answer, callback_data=answer) for answer in answers]
    keyboard.add(*buttons)
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
    Game(user_id=message.from_user.id).end_game()
    bot.send_message(message.chat.id, "Спасибо за честную игру")


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
def message_handler(message):
    """Функция для получения сообщений от пользователя"""
    bot.send_message(message.chat.id, "Чтобы начать игру введи команду /game")


@bot.callback_query_handler(func=lambda call: True)
def check_answer(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    try:
        g = Game(user_id=user_id)
        if g.check_answer(call.data):
            Statistics(user_id=user_id).add_right_answer()
            text = "{emoji} <b>{question}</b>\nВаш ответ: <i>{answer}</i>".format(
                emoji=settings.RIGHT_ANSWER_EMOJI,
                question=call.message.text,
                answer=call.data
            )
        else:
            Statistics(user_id=user_id).add_wrong_answer()
            text = "{emoji} <b>{question}</b>\nВаш ответ: <i>{answer}</i>\nВерный ответ: <i>{right_answer}</i>"
            text = text.format(
                emoji=settings.WRONG_ANSWER_EMOJI,
                question=call.message.text,
                answer=call.data,
                right_answer=g.expected_answer
            )
        bot.edit_message_text(text, chat_id=chat_id, message_id=call.message.message_id, parse_mode='HTML')
        send_question(user_id=user_id)
    except ExpectedAnswerNotFoundException:
        bot.send_message(chat_id, "Чтобы начать игру введи команду /game")


if __name__ == '__main__':
    bot.polling(none_stop=True)
