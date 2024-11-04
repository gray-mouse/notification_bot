import telebot
import schedule
import time
from threading import Thread
from database.models import User
import datetime
import logging


logging.basicConfig(
    filename='bot_logs/bot_logs.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] | %(levelname)s | %(message)s',
    encoding='utf-8'
)


def send_message_to_all_users(bot, message_text):
    users = User.select()
    for user in users:
        try:
            bot.send_message(user.tg_id, message_text)
            logging.info(f"Сообщение отправлено пользователю {user.tg_id}.")
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение пользователю {user.tg_id}: {e}")


def job(bot):
    today = datetime.date.today()
    if today.day == 25:
        message_text = ("Сегодня 25-е число! Время собирать дань.\n"
                        "Подробнее ---> /payment")
        send_message_to_all_users(bot, message_text)
        logging.info("Запланированное сообщение отправлено всем пользователям.")


def schedule_job(bot):
    schedule.every().day.at("12:30").do(job, bot)


def run_scheduler(bot):
    while True:
        schedule.run_pending()
        time.sleep(1)