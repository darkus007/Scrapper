from os import getenv
from sys import argv

from scrapper import HHScrapper
from database import Database


if __name__ == '__main__':
    search_phrase = '+'.join([arg.strip() for arg in argv[1:]])
    if search_phrase and len(search_phrase) > 2:
        scrapper = HHScrapper(search_phrase)
        scrapper.run()
        vacancies = scrapper.vacancies

        database = Database(getenv('MONGO_DOCKER'), 'hh_scrapper', 'vacancy')
        database.replace_many(vacancies)
        del database
    else:
        print('Не указана искомая вакансия. \n'
              'Выполните команду "python3 main.py Искомая вакансия". Например: \n'
              'python3 main.py Python MongoDB')
