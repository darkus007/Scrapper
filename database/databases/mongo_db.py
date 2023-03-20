"""
Модуль для работы с базой данных MongoDB.
Реализованы основные метода чтения и записи.
"""

from os import getenv
from dataclasses import asdict

import pymongo
from pymongo.results import InsertOneResult, InsertManyResult

from .base_database import NoSQLBase
from .data_class import Vacancy
from logger import init_logger, LOGGER_LEVEL

logger = init_logger(__name__, LOGGER_LEVEL)


class MongoDB(NoSQLBase):
    def __init__(self, host, database, collection):
        """
        Класс для работы с базой данных MongoDB.

        :param host: Параметры подключения к MongoDB.
        :param database: Название базы данных.
        :param collection: Название коллекции.
        """
        self.db_name = database
        self.collection_name = collection
        self.db_client = pymongo.MongoClient(host=host,
                                             username=getenv('MONGO_USER', 'root'),
                                             password=getenv('MONGO_USER_PASSWORD', 'example'),
                                             )
        self.current_db = self.db_client[self.db_name]
        self.collection = self.current_db[self.collection_name]

    def __del__(self):
        self.db_client.close()

    def insert_one(self, data: dict) -> InsertOneResult:
        """ Добавляет одн документ в коллекцию. """
        return self.collection.insert_one(data)

    def insert_many(self, data: list[dict]) -> InsertManyResult:
        """ Добавляет документы в коллекцию. """
        return self.collection.insert_many(data)

    def replace_many(self, data: list[dict | Vacancy]) -> tuple[int, int]:
        """
        Обновляет документы в базе данных, если такого документа нет - то создает его.
        :param data: Список словарей или экземпляров dataclass для сохранения в базе данных.
        :return: Количеств обновленных и добавленных записей.
        """
        modified_count = 0
        upsert_count = 0
        for d in data:
            if not isinstance(d, dict):
                d = asdict(d)
            temp = self.collection.replace_one({'_id': d['_id']}, d, upsert=True)
            modified_count += temp.modified_count
            if temp.upserted_id:
                upsert_count += 1
        logger.debug(f'Обновлено {modified_count}, добавлено {upsert_count} записей в базу данных MongoDB.')
        return modified_count, upsert_count

    def drop_collection(self):
        """ Удаляет коллекцию в базе данных. """
        return self.current_db.drop_collection(self.collection_name)

    def drop_database(self):
        """ Удаляет базу данных. """
        self.db_client.drop_database(self.db_name)
