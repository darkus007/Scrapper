"""
Дата-класс представления собранных данных.
"""

from dataclasses import dataclass


@dataclass
class Vacancy:
    vacancy_id: int            # id вакансии
    title: str          # Название вакансии
    price: str          # Предложение по зарплате
    url: str            # Ссылка на вакансию
    date: str           # Дата получения информации о вакансии
    skills: str = None  # Ключевые навыки, которые указал работодатель

    # def __str__(self):
    #     return str(self._id) + self.title + '\t' + \
    #            str(self.price) + '\t' + self.url + '\t' + \
    #            self.date + '\t' + str(self.skills)
