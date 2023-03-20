from os import getenv
from unittest import TestCase

import pymongo

from database.databases.mongo_db import MongoDB


class MongoDBTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.db_client = pymongo.MongoClient(getenv('MONGO_CONNECT'))
        cls.current_db = cls.db_client['test_db']
        cls.collection = cls.current_db['test_coll']

    @classmethod
    def tearDownClass(cls) -> None:
        cls.current_db.drop_collection('test_coll')
        cls.db_client.drop_database('test_db')
        cls.db_client.close()

    def test_insert_one(self):
        input_data = {'param1': 'value1', 'param2': 2, 'param3': 3}
        res = MongoDB(getenv('MONGO_CONNECT'), 'test_db', 'test_coll').insert_one(input_data)
        expected_data = self.collection.find_one(input_data)
        self.assertTrue(res.acknowledged)
        self.assertEqual(input_data, expected_data)

    def test_insert_many(self):
        input_data = [{'param': 'value1', 'param2': 2, 'param3': 3},
                      {'param': 'value2', 'param3': 3, 'param4': 4},
                      {'param': 'value3', 'param4': 4, 'param6': 5},
                      ]
        res = MongoDB(getenv('MONGO_CONNECT'), 'test_db', 'test_coll').insert_many(input_data)
        find_key = {'param': {'$regex': r'\w'}}
        expected_data = list(self.collection.find(find_key))
        self.assertTrue(res.acknowledged)
        self.assertEqual(input_data, expected_data)

    def test_replace_many(self):
        # Для начала добавляем уникальные данные
        # проверяем, что все данные будут добавлены
        input_dat1 = [{'_id': 1, 'param1': 1, 'param2': 1},
                      {'_id': 2, 'param1': 2, 'param2': 2},
                      {'_id': 3, 'param1': 3, 'param2': 3},
                      ]
        res = MongoDB(getenv('MONGO_CONNECT'), 'test_db', 'test_coll').replace_many(input_dat1)
        self.assertEqual(res, (0, 3))       # 0 - изменено, 3 - добавлено

        # Добавляем данные, которые уже существуют
        # проверяем, что существующие будут обновлены, а новые добавлены
        input_dat2 = [{'_id': 1, 'param1': 1, 'param2': 1},
                      {'_id': 2, 'param1': 4, 'param2': 2},
                      {'_id': 3, 'param1': 3, 'param2': 4},
                      {'_id': 4, 'param1': 4, 'param2': 4},
                      ]
        res = MongoDB(getenv('MONGO_CONNECT'), 'test_db', 'test_coll').replace_many(input_dat2)
        self.assertEqual(res, (2, 1))

    def test_drop_collection(self):
        # Создаем коллекцию через добавление записи
        # и проверяем, что она была создана
        input_data = {'param1': 'value1', 'param2': 2, 'param3': 3}
        self.collection.insert_one(input_data)
        self.assertEqual(self.current_db.list_collection_names(), ['test_coll'])

        # Удаляем коллекцию и проверяем, что она была удалена
        MongoDB(getenv('MONGO_CONNECT'), 'test_db', 'test_coll').drop_collection()
        self.assertEqual(self.current_db.list_collection_names(), [])

    def test_drop_database(self):
        # Создаем коллекцию через добавление записи, а через нее базу данных
        # и проверяем, что она была создана
        input_data = {'param1': 'value1', 'param2': 2, 'param3': 3}
        self.collection.insert_one(input_data)
        self.assertTrue('test_db' in self.db_client.list_database_names())

        # Удаляем базу данных и проверяем, что она была удалена
        MongoDB(getenv('MONGO_CONNECT'), 'test_db', 'test_coll').drop_database()
        self.assertTrue('test_db' not in self.db_client.list_database_names())
