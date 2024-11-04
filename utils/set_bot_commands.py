from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS, ADMIN_COMMANDS, ADMIN_ID


def set_default_commands(bot, user_id=None):
    commands = list(DEFAULT_COMMANDS)
    if user_id == int(ADMIN_ID):
        commands += list(ADMIN_COMMANDS)

    bot.set_my_commands([BotCommand(*cmd) for cmd in commands])