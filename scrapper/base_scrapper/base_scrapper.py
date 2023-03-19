from abc import ABC, abstractmethod


class BaseScrapper(ABC):
    """ Базовый класс для парсера """

    @abstractmethod
    def run(self):
        """ Запускает сбор информации. """
        ...
