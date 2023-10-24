import unittest
from remote_execution import app


class TestRemoteExecution(unittest.TestCase):

    def setUp(self) -> None:
        """Настройки приложения"""
        app.config['TESTING'] = False
        app.config['DEBUG'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url: str = '/run_code'

    def test_run_code_fuc_print(self) -> None:
        """Текст выполняет проверку выполнения кода с валидными параметрами."""
        result: str = 'Hello world'
        data: dict = {'timeout': 5, 'code': "print('Hello world')"}
        response = self.app.post(self.base_url, data=data)
        result_test: str = response.text
        self.assertTrue(result in result_test)

    def test_run_code_func_print_syntax_er(self) -> None:
        """Текст выполняет проверку выполнения кода с валидными параметрами, но с синтаксической ошибкой."""
        result: str = 'SyntaxError: invalid syntax.'
        data: dict = {'timeout': 2, 'code': "print(Hello world)"}
        response = self.app.post(self.base_url, data=data)
        result_test: str = response.text
        self.assertTrue(result in result_test)

    def test_run_code_func_max(self) -> None:
        """Текст выполняет проверку выполнения кода с валидными параметрами."""
        result: str = '6'
        data: dict = {'timeout': 1, 'code': "x=max(5, 6);print(x)"}
        response = self.app.post(self.base_url, data=data)
        result_test: str = response.text
        self.assertTrue(result in result_test)

    def test_run_code_empty_timeout(self) -> None:
        """Текст выполняет проверку выполнения кода с отсутствием параметра timeout."""
        result: str = 'Invalid input'
        status: str = '400 BAD REQUEST'
        data: dict = {'timeout': None, 'code': "x=max(5, 6);print(x)"}
        response = self.app.post(self.base_url, data=data)
        result_test = response.text
        self.assertTrue(result in result_test)
        self.assertEqual(status, response.status)

    def test_run_code_timeout(self) -> None:
        """Текст выполняет проверку выполнения кода с задержкой по времени."""
        result: str = 'Timeout'
        status: str = '200 OK'
        data: dict = {'timeout': 2, 'code': "from time import sleep; sleep(6); print('func is late')"}
        response = self.app.post(self.base_url, data=data)
        result_test: str = response.text
        self.assertTrue(result in result_test)
        self.assertEqual(status, response.status)


if __name__ == '__main__':
    unittest.main()
