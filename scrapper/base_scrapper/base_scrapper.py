from abc import ABC, abstractmethod


class BaseScrapper(ABC):
    """ Базовый класс парсера. """

    @abstractmethod
    def run(self):
        """ Запускает сбор информации. """
        ...

    @abstractmethod
    def get_result(self):
        """ Возвращает результат сбора информации. """
        ...
