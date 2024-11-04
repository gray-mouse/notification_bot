from loader import bot
from threading import Thread
from utils.set_bot_commands import set_default_commands
from utils.scheduler import schedule_job, run_scheduler
import logging
import sys
import handlers
from config_data.config import ADMIN_ID

logging.basicConfig(
    filename='bot_logs/bot_logs.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] | %(levelname)s | %(message)s',
    encoding='utf-8'
)

if __name__ == "__main__":
    try:
        logging.info('Запуск бота...')
        set_default_commands(bot, user_id=int(ADMIN_ID))
        schedule_job(bot)
        Thread(target=run_scheduler, args=(bot,)).start()
        logging.info('Запущен schedule_job')
        bot.infinity_polling()
        logging.info('Бот остановлен')
    except Exception as e:
        logging.error(f'Ошибка в работе бота: {e}', exc_info=True)
        sys.exit(1)

