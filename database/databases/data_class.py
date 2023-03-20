"""
Дата-класс представления собранных данных.
"""

from dataclasses import dataclass


@dataclass
class Vacancy:
    _id: int            # id вакансии
    title: str          # Название вакансии
    price: str          # Предложение по зарплате
    url: str            # Ссылка на вакансию
    date: str           # Дата получения информации о вакансии
    skills: str = None  # Ключевые навыки, которые указал работодатель
