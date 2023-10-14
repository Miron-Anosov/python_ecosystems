import unittest
from module_03_ci_culture_beginning.homework.hw3.accounting import app, manager


class MyTestCase(unittest.TestCase):
    """
    Класс тестов для проверки функциональности приложения учёта финансов.

    """
    storage: dict = {
        '2021-01-15': 100,
        '2021-03-05': 150,
        '2021-05-20': 200,
        '2021-05-10': 80,
        '2021-05-02': 120,
        '2021-10-15': 90,
        '2021-12-08': 110,
        '2022-02-25': 180,
        '2022-02-14': 70,
        '2022-06-30': 130,
        '2022-02-18': 160,
        '2022-10-05': 210,
        '2022-12-20': 95,
        '2023-02-08': 200,
        '2023-04-22': 240,
        '2023-06-15': 115,
        '2023-08-03': 170,
        '2023-09-28': 190,
        '2023-11-10': 220,
        '2023-12-25': 250
    }

    def setUp(self):
        """
        Настройка тестового окружения перед запуском каждого теста.
        """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.url_add = '/add/'
        self.url_calculate = '/calculate/'

    def tearDown(self):
        """
        Очищаем словарь после каждого теста
        """
        manager.storage = {}

    def test_add_working_correct(self):
        """
        Тест проверяет добавление данных в словарь.
        """
        for date, rub in self.storage.items():
            response_pattern = f'Created new data: new date:<b>{date}</b> rub:<b>{rub}</b>'
            with self.subTest(response_patern=response_pattern):
                url = ''.join(f'{self.url_add}{date}/{rub}')
                response = self.app.get(url)
                response_text = response.data.decode()
                self.assertTrue(response_pattern in response_text)

    def test_update_dict(self):
        """
        Тест проверяет обновление данных в словаре.
        """

        for date, rub in self.storage.items():
            response_pattern = f'Datas was update: date:<b>{date}</b> rub:<b>{self.storage.get(date) * 2}</b>'
            with self.subTest(response_patern=response_pattern):
                url = ''.join(f'{self.url_add}{date}/{rub}')
                self.app.get(url)
                response = self.app.get(url)
                response_text = response.data.decode()
                self.assertTrue(response_pattern in response_text)

    def test_date_not_correct(self):
        """
        Текст проверяет отработку исключения ValueError при вводе не корректной даты.
        """
        date = '2022-02-31'
        number = 10
        response_pattern = f"Datas didn't update. Datas aren't correct. ({date=}: {number=}) <br> " \
                           f"Format date: <b>YYYY-MM-DD</b><br>" \
                           f"Format number <b>integer or float</b>"
        url = ''.join(f'{self.url_add}{date}/{number}')
        response = self.app.get(url)
        response_text = response.data.decode()
        self.assertTrue(response_pattern in response_text)

    def test_add_not_correct_date_not_found(self):
        """
        Текст проверяет статус ответа от сервера при вводе не корректного числа.
        """
        date = '2022-02-31'
        number = 'ten'
        status = '404 NOT FOUND'
        url = ''.join(f'{self.url_add}{date}/{number}')
        response = self.app.get(url)
        real_status = response.status
        self.assertEqual(real_status, status)

    def test_calculate_year(self):
        """
        Тест проверяет результат запроса данных за период в 1 год.
        """
        year = 2021
        count_rub = 850
        for date, rub in self.storage.items():
            url = ''.join(f'{self.url_add}{date}/{rub}')
            self.app.get(url)
        pattern_response = f'Expenses for <b>{2021}</b>: rub:<b>{count_rub}</b>'
        url = ''.join(f'{self.url_calculate}{year}')
        response = self.app.get(url)
        response_text = response.data.decode()
        self.assertTrue(pattern_response in response_text)

    def test_calculate_month(self):
        """
        Тест проверяет результат запроса данных за период в 1 месяц.
        """
        year = '2022'
        month = '02'
        count_rub = 410
        for date, rub in self.storage.items():
            url = ''.join(f'{self.url_add}{date}/{rub}')
            self.app.get(url)
        pattern_response = f'Expenses for <b>{year}-{month}</b>: rub:<b>{count_rub}</b>'
        url = ''.join(f'{self.url_calculate}{year}/{month}')
        response = self.app.get(url)
        response_text = response.data.decode()
        self.assertTrue(pattern_response in response_text)

    def test_add_empty_date_and_num_not_found(self):
        """
        Тест проверяет результат добавления данных при их отсутствии.
        """
        year = ''
        month = ''
        status = '404 NOT FOUND'
        url = ''.join(f'{self.url_calculate}{year}/{month}')
        response = self.app.get(url)
        real_status = response.status
        self.assertEqual(real_status, status)

    def test_calculate_empty_dict(self):
        """
        Тест проверяет результат запроса данных за период год/месяц при отсутствии данных.
        """
        year = '2022'
        response_pattern = f"You didn't have expenses for <b>{year}</b>"
        url = ''.join(f'{self.url_calculate}{year}')
        response = self.app.get(url)
        response_text = response.data.decode()
        self.assertTrue(response_pattern in response_text)


if __name__ == '__main__':
    unittest.main()
