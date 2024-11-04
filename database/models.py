from peewee import SqliteDatabase, Model, CharField, IntegerField
import logging


logging.basicConfig(
    filename='bot_logs/bot_logs.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] | %(levelname)s | %(message)s',
    encoding='utf-8'
)


db = SqliteDatabase("database/database.db")


class User(Model):
    tg_id = IntegerField(unique=True)
    username = CharField()

    class Meta:
        database = db

class ServerConfig(Model):
    cost = IntegerField(default=450)

    class Meta:
        database = db


db.connect()
db.create_tables([User, ServerConfig], safe=True)


def initialize_server_config():
    if not ServerConfig.select().exists():
        ServerConfig.create(cost=450)
        logging.info("Инициализация конфигурации сервера: запись создана с дефолтной стоимостью 450")
    else:
        logging.info("Инициализация конфигурации сервера: запись уже существует")

initialize_server_config()


def get_current_cost():
    current_cost = ServerConfig.get().cost
    logging.info(f"Получение текущей стоимости: {current_cost}")
    return current_cost


def update_cost(new_cost):
    config = ServerConfig.get_or_none()
    if config is not None:
        config.cost = new_cost
        config.save()
        logging.info(f"Стоимость обновлена на: {new_cost}")
    else:
        ServerConfig.create(cost=new_cost)
        logging.info(f"Создана новая запись с стоимостью: {new_cost}")