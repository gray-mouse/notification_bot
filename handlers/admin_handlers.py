from telebot.types import Message
from loader import bot
from config_data.config import ADMIN_COMMANDS, ADMIN_ID
from database.models import User, update_cost
import logging



logging.basicConfig(
    filename='bot_logs/bot_logs.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] | %(levelname)s | %(message)s',
    encoding='utf-8'
)

def is_admin(message):
    return message.from_user.id == int(ADMIN_ID)


@bot.message_handler(commands=["admin_help"])
def bot_help(message: Message):
    if is_admin(message):
        text = [f"/{command} - {desk}" for command, desk in ADMIN_COMMANDS]
        bot.reply_to(message, "\n".join(text))


@bot.message_handler(commands=['view_users'])
def view_users(message: Message):
    if is_admin(message):
        users = User.select()
        if users:
            user_list = "\n".join([f"ID: {user.tg_id} ---> Username: {user.username}" for user in users])
            bot.send_message(message.chat.id, f"Список пользователей:\n{user_list}")
        else:
            bot.send_message(message.chat.id, "Нет зарегистрированных пользователей.")
    else:
        bot.send_message(message.chat.id, "Команда доступна только администратору.")


@bot.message_handler(commands=['delete_user'])
def delete_user(message: Message):
    if is_admin(message):
        try:
            user_id = int(message.text.split()[1])
            user = User.get(User.tg_id == user_id)
            user.delete_instance()
            bot.send_message(message.chat.id, f"Пользователь с ID {user_id} удален.")
        except IndexError:
            bot.send_message(message.chat.id, "Пожалуйста, укажите ID пользователя. Пример: /delete_user 12345")
        except User.DoesNotExist:
            bot.send_message(message.chat.id, f"Пользователь с ID {user_id} не найден.")
        except ValueError:
            bot.send_message(message.chat.id, "ID пользователя должен быть числом.")
    else:
        bot.send_message(message.chat.id, "Команда доступна только администратору.")


@bot.message_handler(commands=["set_cost"])
def set_total_cost(message: Message):
    if is_admin(message):
        try:
            new_cost = int(message.text.split()[1])
            total_cost = new_cost
            update_cost(total_cost)  # Обновляем стоимость в базе
            bot.reply_to(message, f"Новая стоимость аренды сервера установлена: {total_cost} руб.")
            logging.info(f"Администратор {message.from_user.username} изменил стоимость аренды на {total_cost}.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Пожалуйста, введите стоимость после команды /set_cost, например: /set_cost 500")
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        logging.warning(f"Пользователь {message.from_user.username} попытался изменить стоимость аренды.")
