# Scrapper
Парсер сайта HH.ru. Ищет предложения работодателей по указанным вакансиям и сохраняет в базу данных MongoDB для дальнейшего анализа.
База данных запускается в Docker, также запускается вэб-интерфейс Mongo Express для удобной работы с базой.

При разработке приложения использованы: \
[MongoDB](https://www.mongodb.com/), \
[Mongo Express](https://github.com/mongo-express/mongo-express), \
[selenium](https://pypi.org/project/selenium/), \
[requests](https://pypi.org/project/requests/), \
[BeautifulSoup](https://pypi.org/project/beautifulsoup4/), 
[lxml](https://pypi.org/project/lxml/), \
[fake-useragent](https://pypi.org/project/fake-useragent/), \
[Docker](https://www.docker.com/).

Полный список в фале `requirements.txt`.

###Описание структуры базы данных
```
_id: int            # id вакансии
title: str          # Название вакансии
price: str          # Предложение по зарплате
url: str            # Ссылка на вакансию
date: str           # Дата получения информации о вакансии
skills: str         # Ключевые навыки, которые указал работодатель
```

База данных [MongoDB](https://www.mongodb.com/) запускается в [Docker](https://www.docker.com/) контейнере.

### Установка и запуск
Приложение написано на [Python v.3.11](https://www.python.org).
1. Скачайте Scrapper на Ваше устройство любым удобным способом (например Code -> Download ZIP, распакуйте архив).
2. Скачайте [chromedriver](https://chromedriver.chromium.org/downloads) и положите его в папку `HHScrapper/scrapper/browser`. 
Качайте из Current Releases ту версию, которая подходит для Вашей операционной системы, узнать версию можно введя в адресной строке браузера [Chrome](https://www.google.com/intl/ru_ru/chrome/) `chrome://settings/help`.
3. Установите [Docker](https://www.docker.com/), если он у Вас еще не установлен.
4. Выполните команду `export MONGO_CONNECT="mongodb://root:example@127.0.0.1:27017/"`
5. Выполните команду `docker-compose up -d --build`
6. Создайте виртуальное окружение `python3 -m venv venv`
7. Активируйте виртуальное окружение `. ./venv/bin/activate`
8. Установите необходимые пакеты и зависимости `pip3 install -r requirements.txt`
9. Теперь можно пользоваться приложением, для этого выполните `python3 main.py Название вакансии`
10. По адресу http://127.0.0.1:8081/ доступен вэб-интерфейс базы данных с собранной информацией.

Далее для сбора информации по интересующим вакансиям, достаточно выполнять только шаг № 9. 
Например, для поиска вакансий `Python Django` запускаем `python3 main.py Python Django`.

Вакансии, полученные разными поисками дублироваться не будут! (например запрашиваем `python3 main.py Python Django` затем `python3 main.py Python`, 
при данных запросах HH выдаст много повторяющихся вакансий, часть из них уже будет в базе от первого запроса, по результатам выполнения второго запроса 
добавятся только новые вакансии).

Внимание! Данные собираются очень медленно, так как HH.ru блокирует IP с которых идут частые запросы на их сайт. 
По этой причине установлена большая задержка по 5 секунд между запросами. Так для 100 вакансий, по 50 вакансий на страницу будет 
два запроса на просмотр страниц и 100 запросов для прохода по каждой вакансии, итого 510 секунд = 8 минут 30 секунд только для 100 вакансий!

Для остановки и удаления контейнеров выполните `docker-compose down`. Это также удалит все собранные данные. 
Для полной очистки системы [удалите образы (images)](https://docs.docker.com/engine/reference/commandline/image_rm/).