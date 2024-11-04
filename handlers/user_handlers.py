from telebot import types
from telebot.types import Message, BotCommand
from loader import bot
from config_data.config import DEFAULT_COMMANDS, ADMIN_COMMANDS, ADMIN_ID
from database.models import User, get_current_cost
from peewee import IntegrityError
import logging


logging.basicConfig(
    filename='bot_logs/bot_logs.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] | %(levelname)s | %(message)s',
    encoding='utf-8'
)



def set_commands_for_user(bot, user_id):
    commands = list(DEFAULT_COMMANDS)
    if int(user_id) == int(ADMIN_ID):
        commands += list(ADMIN_COMMANDS)
    bot.set_my_commands([BotCommand(*cmd) for cmd in commands])


# /start
@bot.message_handler(commands=["start"])
def handle_start(message: Message) -> None:
    tg_id = message.from_user.id
    username = message.from_user.username

    try:
        User.create(
            tg_id=tg_id,
            username=username,
        )
        bot.reply_to(message, f"Добро пожаловать, дружок {username}! Регистрация прошла успешно.\n"
                              f"Нажми на ---> /about чтобы узнать подробности.")
        logging.info(f"Пользователь {username} прошел регистрацию.")
    except IntegrityError:
        bot.reply_to(message, f"Рад снова тебя видеть, дружок {username}!\nНажми на ---> /about чтобы узнать подробности.")

    set_commands_for_user(bot, tg_id)


# /about
@bot.message_handler(commands=["about"])
def bot_about(message: Message):
    bot.reply_to(message, f"Каждый месяц, 25-го числа бот отправляет оповещения об оплате "
                          f"доступа к VPS-серверу NL-Server.\n"
                          f"Стоимость оплаты рассчитывается исходя из формулы:\n"
                          f"СТОИМОСТЬ АРЕНДЫ СЕРВЕРА / КОЛИЧЕСТВО ПОЛЬЗОВАТЕЛЕЙ\n"
                          f"Ознакомься с функциями бота, нажми на ---> /help\n"
                          f"Появились вопросы? Напиши владельцу бота.")
    logging.info(f"Пользователь {message.from_user.username} узнал подробности о боте.")


# /help
@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))


# /payment
@bot.message_handler(commands=["payment"])
def bot_payment(message: Message):
    total_cost = get_current_cost()
    user_count = User.select().count()

    if user_count > 0:
        average_cost = total_cost / user_count
        response = (f"Стоимость аренды сервера на данный момент: {total_cost} руб.\n"
                    f"Количество пользователей на данный момент: {user_count}\n"
                    f"Стоимость оплаты для каждого пользователя: {average_cost:.2f} руб.\n"
                    f"Оплатить можно переводом владельцу бота.\n"
                    f"Не знаешь что делать дальше? Тыкни сюда ---> /about")
    else:
        response = "Нет пользователей в базе данных."

    bot.reply_to(message, response)
    logging.info(f"Пользователь {message.from_user.username} Узнал стоимость оплаты.")


#Обработка невалидных сообщений от пользователя
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_non_command_message(message: types.Message):
    try:
        raise ValueError("Неизвестная команда или сообщение")
    except ValueError as e:
        response = (f"Таких слов или команд как '{message.text}' не знаю.\n"
                    f"Если потерялся, жми сюда ---> /help ")
        bot.reply_to(message, response)
        logging.info(f"Пользователь {message.from_user.username} отправил невалидное сообщение: {message.text} - Ошибка: {e}")
