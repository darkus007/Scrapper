"""
Модуль собирает информация по вакансиям с сайта HH.ru:
- id вакансии;
- Название вакансии;
- Предложение по цене;
- Ссылка на вакансию;
- Ключевые навыки, которые указал работодатель.

При частых запросах с одного IP, сайт HH.ru выдает пустую страницу
с проверкой на робота (captcha). По этой причине установлены длительные
задержки между запросами (SLEEP_BETWEEN_REQUESTS).
"""

import re
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup

from logger import init_logger, LOGGER_LEVEL
from database.databases import Vacancy
from .base_scrapper import BaseScrapper, SeleniumMixin, RequestsMixin

logger = init_logger(__name__, LOGGER_LEVEL)

URL_PREFIX = "https://hh.ru/search/vacancy?text="
URL_SUFFIX = "&salary=&area=1&ored_clusters=true&page="

SLEEP_BETWEEN_REQUESTS = 5

HH_SCRAPPER_DEBUG = True  # если True, то собирает данные НЕ полностью (для экономии времени)


class HHScrapper(BaseScrapper, SeleniumMixin, RequestsMixin):
    def __init__(self, vacancy: str):
        """
        Собирает информацию о вакансиях с сайта HH.ru
        - id вакансии;
        - Название вакансии;
        - Предложение по цене;
        - Ссылка на вакансию;
        - Ключевые навыки, которые указал работодатель;
        - Дата сбора информации.
        Для запуска необходимо вызвать метод "run()".
        Результат работы можно получить из "vacancies".

        :param vacancy: Название искомой вакансии.
        """
        BaseScrapper.__init__(self)
        SeleniumMixin.__init__(self)
        RequestsMixin.__init__(self)
        self.url = URL_PREFIX + vacancy + URL_SUFFIX
        self.vacancies: list[Vacancy] = []  # хранит результат сбора данных

    def __get_general_info(self) -> None:
        """
        Проходит по всем страницам и собирает основную информацию о вакансиях.
        Добавляет данные в свойство self.vacancies.
        :return: None;
        """
        html = self.selenium_get(url=self.url + '0')

        soup = BeautifulSoup(html, 'lxml')

        try:
            total_pages = int(soup.find_all('a', class_='bloko-button')[-2].text)  # всего страниц
        except (IndexError, ValueError):
            total_pages = 0
        try:
            total_vacancies = soup.find('h1', attrs={'data-qa': 'bloko-header-3',
                                                     'class': 'bloko-header-section-3'}).text
        except Exception:
            total_vacancies = ''
        logger.debug(total_vacancies)
        logger.debug(f'Всего страниц {total_pages}.')

        all_vacancy_on_page = soup.find_all(class_="vacancy-serp-item__layout")
        self.__scrap_general_info(all_vacancy_on_page)  # собираем информацию с первой страницы
        logger.debug(f'Пройдено 1 страница из {total_pages}. Вакансий {len(self.vacancies)}.')

        for page in range(1, total_pages):  # проходим по всем остальным страницам и собираем информацию
            sleep(SLEEP_BETWEEN_REQUESTS)
            html = self.selenium_get(url=self.url + str(page))
            soup = BeautifulSoup(html, 'lxml')
            all_vacancy_on_page = soup.find_all(class_="vacancy-serp-item__layout")
            self.__scrap_general_info(all_vacancy_on_page)
            logger.debug(f'Пройдено {page + 1} страниц(ы) из {total_pages}. Вакансий {len(self.vacancies)}.')

            if HH_SCRAPPER_DEBUG:  # прерываемся для экономии времени при отладке
                break

    def __scrap_general_info(self, all_vacancy_on_page) -> None:
        """
        Собирает основную информацию о вакансиях со страницы
        (Название вакансии, Предложение по цене, Ссылка на вакансию).

        :param all_vacancy_on_page: Результат работы BeautifulSoup
        по поиску блоков div с информацией о вакансиях.

        :return: None; Добавляет данные в свойство self.vacancies.
        """
        date = datetime.now().strftime('%Y-%m-%d')
        for item in all_vacancy_on_page:
            price_temp = item.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            _url = item.find(class_='serp-item__title').get('href')
            vacancy = Vacancy(
                title=item.find(class_='serp-item__title').text,
                url=_url,
                _id=int(re.findall(r'\d{4,10}', _url)[0]),
                # replace(u"\u202F", " ") - заменяем неразрывные пробелы "NNBSP" на обычные
                price=None if not price_temp else price_temp.text.replace(u"\u202F", " "),
                date=date
            )
            self.vacancies.append(vacancy)

    def __get_skills(self) -> None:
        """
        Проходит по всем URL найденных вакансий и
        добавляет в каждую информацию о Ключевых навыках.
        Обновляет данные в свойстве self.vacancies.

        :return: None;
        """
        total_vacancies = len(self.vacancies)
        current_vacancy = 1
        logger.debug('Собираем информацию о ключевых навыках:')
        for vacancy in self.vacancies:
            html = self.requests_get(vacancy.url)
            soup = BeautifulSoup(html, 'lxml')
            src_skills = soup.find_all('div', attrs={'class': 'bloko-tag bloko-tag_inline',
                                                     'data-qa': 'bloko-tag bloko-tag_inline skills-element'})
            # replace(u"\u202F", " ") - заменяем неразрывные пробелы "NNBSP" на обычные
            skills = ', '.join(skl.text.replace(u"\u202F", " ") for skl in src_skills)
            vacancy.skills = skills
            logger.debug(f'[{current_vacancy}|{total_vacancies}]\t{skills}')
            current_vacancy += 1
            sleep(SLEEP_BETWEEN_REQUESTS)

            if HH_SCRAPPER_DEBUG:  # прерываемся для экономии времени при отладке
                break

    def run(self):
        """ Запускает сбор информации. """
        logger.info('Начало сбора информации.')
        self.__get_general_info()
        self.__get_skills()
        logger.info(f'Конец сбора информации. Получено {len(self.vacancies)} записей.')

    def get_result(self):
        """ Возвращает результат сбора информации. """
        return self.vacancies
