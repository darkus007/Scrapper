"""
Сохраняет информацию в базе данных.

Создан для быстрой смены базы данных,
достаточно изменить базовый класс на другой.
"""

from .databases import MongoDB


class Database(MongoDB):
    """ Сохраняет информацию в базу данных MongoDB. """
    ...
