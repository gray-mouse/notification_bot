import os
from dotenv import load_dotenv, find_dotenv
import logging

logging.basicConfig(
    filename='bot_logs/bot_logs.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] | %(levelname)s | %(message)s',
    encoding='utf-8'
)

if not find_dotenv():
    exit(logging.error("Переменные окружения не загружены т.к отсутствует файл .env"))
else:
    load_dotenv()
    logging.info("Переменные окружения загружены из файла .env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("about", "Вывести справку"),
    ("payment", "Узнать стоимость оплаты"),
    ("help", "Функции бота")
)

ADMIN_COMMANDS = (
    ("view_users", "Просмотр пользователей"),
    ("delete_user", "Удалить пользователя. Укажите ID пользователя. Пример: /delete_user 12345"),
    ("admin_help", "Справка по командам админа"),
    ("set_cost", "Установить стоимость аренды сервера")
)