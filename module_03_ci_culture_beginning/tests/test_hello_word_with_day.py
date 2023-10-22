import unittest

import freezegun

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class TestDayOfWeek(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    @freezegun.freeze_time("2023-10-02")
    def test_monday_true(self):
        """
        Проверяем на соответствие понедельника. Позитивный текст.
        """
        monday = 'Хорошего понедельника'
        user = 'user_default'
        response = self.app.get(''.join(self.base_url + user))
        response_text = response.data.decode()
        self.assertTrue(monday in response_text)

    @freezegun.freeze_time("2023-10-03")
    def test_false_day(self):
        """
        Проверяем на соответствие понедельника. Негативный текст.
        """
        monday = 'Хорошего понедельника'
        user = 'user_default'
        response = self.app.get(''.join(self.base_url + user))
        response_text = response.data.decode()
        self.assertFalse(monday in response_text)

    @freezegun.freeze_time("2023-10-03")
    def test_bug_name(self):
        """
        Проверяем на соответствие Имени. Негативный текст.
        """
        monday = 'Хорошего понедельника'
        response = self.app.get(''.join(self.base_url + monday))
        response_text = response.data.decode()
        self.assertFalse('user_default' in response_text)

    @freezegun.freeze_time("2023-10-03")
    def test_tuesday_true(self):
        """
        Проверяем на соответствие вторника. Позитивный текст.
        """
        tuesday = 'Хорошего вторника'
        user = 'user_default'
        response = self.app.get(''.join(self.base_url + user))
        response_text = response.data.decode()
        self.assertTrue(tuesday in response_text)

    @freezegun.freeze_time("2023-10-04")
    def test_wednesday(self):
        """
        Проверяем на соответствие среды. Позитивный текст.
        """
        wednesday = 'Хорошей среды'
        user = 'user_default'
        response = self.app.get(''.join(self.base_url + user))
        response_text = response.data.decode()
        self.assertTrue(wednesday in response_text)

    @freezegun.freeze_time("2023-10-05")
    def test_thursday(self):
        """
        Проверяем на соответствие четверга. Позитивный текст.
        """
        thursday = 'Хорошего четверга'
        user = 'user_default'
        response = self.app.get(''.join(self.base_url + user))
        response_text = response.data.decode()
        self.assertTrue(thursday in response_text)

    @freezegun.freeze_time("2023-10-06")
    def test_friday(self):
        """
        Проверяем на соответствие пятницы. Позитивный текст.
        """
        friday = 'Хорошей пятницы'
        user = 'user_default'
        response = self.app.get(''.join(self.base_url + user))
        response_text = response.data.decode()
        self.assertTrue(friday in response_text)

    @freezegun.freeze_time("2023-10-07")
    def test_saturday(self):
        """
        Проверяем на соответствие субботы. Позитивный текст.
        """
        saturday = 'Хорошей субботы'
        user = 'user_default'
        response = self.app.get(''.join(self.base_url + user))
        response_text = response.data.decode()
        self.assertTrue(saturday in response_text)

    @freezegun.freeze_time("2023-10-08")
    def test_sunday(self):
        """
        Проверяем на соответствие воскресенья. Позитивный текст.
        """
        sunday = 'Хорошего воскресенья'
        user = 'user_default'
        response = self.app.get(''.join(self.base_url + user))
        response_text = response.data.decode()
        self.assertTrue(sunday in response_text)


if __name__ == '__main__':
    unittest.main()
