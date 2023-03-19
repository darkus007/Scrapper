from os import path
from pathlib import Path
from time import sleep

from selenium import webdriver

SLEEP_SECONDS = 5
IMPLICITLY_WAIT_SECONDS = 10

CURRENT_PATH = Path(__name__).resolve().parent.parent
CHROME_DRIVER_PATH = path.join(CURRENT_PATH, 'browser/chromedriver')


class SeleniumMixin:
    def __init__(self):
        self.__options = webdriver.ChromeOptions()
        # for ChromeDriver version 79.0.3945.16 or over
        # отключаем обнаружение, что мы заходим с chromedriver-а
        self.__options.add_argument("--disable-blink-features=AutomationControlled")
        self.__options.headless = True
        self.__driver = webdriver.Chrome(
            executable_path=CHROME_DRIVER_PATH,
            options=self.__options
        )

    def selenium_get(self, url: str) -> str:
        """ Возвращает HTML страницу по указанному url """
        self.__driver.get(url=url)
        sleep(SLEEP_SECONDS)
        # ждем пока загрузится вся страница или истечет время IMPLICITLY_WAIT_SECONDS
        self.__driver.implicitly_wait(IMPLICITLY_WAIT_SECONDS)
        return self.__driver.page_source

    def __del__(self):
        """ Закрываем selenium webdriver. """
        self.__driver.close()  # Закрываем окно
        self.__driver.quit()  # Закрываем браузер
