"""Параметры конфигурации для работы бота"""

# Токен для авторизации в API телеграма
TOKEN = '427290349:AAFMBOb2E-yQIANQAYMz7zwqKE6a25xEhPw'

# Относительный путь к файлу с переводами слов
DATABASE_NAME = 'db/english_dictionary.sqlite3'

# Относительный путь к файлам для хранения данных статистики в виде хеш-таблиц
STATISTICS_SHELVE_NAME = 'shelve/statistics'

# Относительный путь к файлам для хранения правильного ответа на вопрос заданный пользователю
SHELVE_NAME = 'shelve/estimate_answers'

# Эмоция, которая добавляется к правильному ответу
RIGHT_ANSWER_EMOJI = chr(9989)

# Эмоция, которая добавляется к неправильному ответу
WRONG_ANSWER_EMOJI = chr(10060)
