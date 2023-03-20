import json
from dataclasses import asdict

from scrapper import HHScrapper
from database import Database


if __name__ == '__main__':
    scrapper = HHScrapper('Python+django')
    scrapper.run()
    vacancies = scrapper.vacancies

    print(vacancies)

    with open("vacancies.json", 'a') as file:
        for vac in vacancies:
            json.dump(asdict(vac), file, indent=4, ensure_ascii=False)
