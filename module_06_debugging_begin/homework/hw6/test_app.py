import unittest
from module_06_debugging_begin.homework.hw6.app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_not_found(self):
        """Текст проверяет наличие ключевых слов, которые отвечают за ссылки"""
        links = ['about', 'index', 'cats', 'dogs']
        result = self.app.get()
        text = result.text
        for page in links:
            self.assertTrue(page in text)

    def test_not_found_negative(self):
        """Текст проверяет отсутствие маршрутов, которые не доступны get запросом"""
        route: str = "static"
        result = self.app.get()
        text = result.text
        self.assertFalse(route in text)


if __name__ == '__main__':
    unittest.main()
