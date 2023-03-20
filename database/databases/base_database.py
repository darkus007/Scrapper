from abc import ABC, abstractmethod

from .data_class import Vacancy


class NoSQLBase(ABC):

    @abstractmethod
    def insert_one(self, data: dict) -> object:
        """ Добавляет одн документ в коллекцию (таблицу). """
        ...

    @abstractmethod
    def insert_many(self, data: list[dict]) -> object:
        """ Добавляет документы в коллекцию (таблицу). """
        ...

    @abstractmethod
    def replace_many(self, data: list[dict | Vacancy]) -> tuple[int, int]:
        """
        Обновляет документы в базе данных, если такого документа нет - то создает его.
        :param data: Список словарей или экземпляров dataclass для сохранения в базе данных.
        :return: Количеств обновленных, количество добавленных записей.
        """
        ...

    @abstractmethod
    def drop_database(self):
        """ Удаляет базу данных. """
        ...

    @abstractmethod
    def drop_collection(self):
        """ Удаляет коллекцию (таблицу) в базе данных. """
        ...
