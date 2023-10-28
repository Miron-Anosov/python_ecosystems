"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app


class TestRegistration(unittest.TestCase):
    """
    Дочерний класс от юнит-теста TestCase, выполняет роль применения функционала для тестирования
    и дальнейшего поддерживания кода.

     Attributes:
         emails_not_correct: tuple: Тестовые значения email.
         data_user: dict: Тестовое значение валидных данных.
         Ответы сервера на Post запросы:
             email_empty_text: str:
             email_invalid_text: str:
             phone_empty_text: str:
             phone_invalid_text: str:
             phone_invalid_length: str:
             address_empty_text: str:
             address_short_text: str:
             name_empty_text: str:
             index_empty_text: str:
             index_invalid: str:

     Notes:
         Для запуска в консоли:
        curl -H "Content-Type: application/json" -d '{"email": "cot@cot.com", "phone": 9993993939, "address": "city",
         "name": "Cat", "index" : 333333, "comment" : "text"}' 'http://127.0.0.1:5000/registration'
    """
    emails_not_correct: tuple = (
        '111', '--', '@', '@ ', ' @ ', 'r@', '@2', 'r@r', 'R@r.', 'r @r.', 'r@com', '@cot.com',
        'cot @cot . com', 'cot@@cot.com', 'cot,@cot.com', 'cot@,cot.com', 'cot@cot.com@', '@cot@cot.com')

    data_user: dict = {'email': 'cot@cot.com', 'phone': 9993993939, 'address': 'city', 'name': 'Cat',
                       'index': 333333, 'comment': 'text'}

    email_empty_text: str = "The email can't be empty"
    email_invalid_text: str = "The email doesn't correct"
    phone_empty_text: str = "The phone can't be empty"
    phone_invalid_text: str = 'The phone is invalid'
    phone_invalid_length: str = 'The phone must be length only 10 numbers'
    address_empty_text: str = "The address can't be empty"
    address_short_text: str = 'The address is too short'
    name_empty_text: str = "The name can't be empty"
    index_empty_text: str = "The index can't be empty"
    index_invalid: str = 'The index length invalid'

    data_valid_text: str = "Successfully registered user cot@cot.com with phone +79993993939"

    def setUp(self) -> None:
        """Настройка тестового окружения."""
        app.config["TESTING"] = False
        app.config["DEBUG"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url: str = '/registration'

    @classmethod
    def tearDown(cls) -> None:
        """Сброс параметров тестового окружения."""
        cls.data_user: dict = {'email': 'cot@cot.com', 'phone': 9993993939, 'address': 'city', 'name': 'Cat',
                               'index': 333333, 'comment': 'text'}

    def test_data_valid(self) -> None:
        """Позитивный тест со всеми полями данных."""
        status: str = '200'
        response_not_correct: str = self.data_valid_text
        response = self.app.post(self.base_url, data=self.data_user)

        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_email_invalid(self) -> None:
        """Негативный тест, проверка валидности почтовых логинов с применением не корректных данных."""
        status: str = '400'
        response_not_correct = self.email_invalid_text
        with self.subTest(response_not_correct=response_not_correct):
            for email in self.emails_not_correct:
                self.data_user['email'] = email
                response = self.app.post(self.base_url, data=self.data_user)
                self.assertTrue(response_not_correct in response.text)
                self.assertTrue(status in response.status)

    def test_email_empty(self) -> None:
        """Негативный тест, проверка валидности почтовых логинов с применением пустой строки. """
        status = '400'
        response_not_correct = self.email_empty_text
        self.data_user['email'] = ''
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_email_empty_str(self) -> None:
        """Негативный тест, проверка валидности почтовых логинов с применением пробелов. """
        status = '400'
        response_not_correct = self.email_invalid_text
        self.data_user['email'] = '  '
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_phone_empty_(self) -> None:
        """Негативный тест, проверка валидности номера телефона с применением отсутствия данных. """
        status = '400'
        response_not_correct = self.phone_empty_text
        self.data_user.pop('phone')
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_phone_short_number(self) -> None:
        """Негативный тест, проверка валидности номера телефона с применением недостающих значений """
        status = '400'
        response_not_correct = self.phone_invalid_length
        self.data_user['phone'] = 939_939_65_4
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_phone_long(self) -> None:
        """Негативный тест, проверка валидности телефона с применением избыточно-длинного значения."""
        status = '400'
        response_not_correct = self.phone_invalid_text
        self.data_user['phone'] = 939_939_65_44_4
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_phone_negative_number(self) -> None:
        """Негативный тест, проверка валидности телефона с применением отрицательных числовых значений."""
        status = '400'
        response_not_correct = self.phone_invalid_text
        self.data_user['phone'] = -939_393_93_93
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_phone_valid(self) -> None:
        """Позитивный тест. Проверка на применение корректного телефонного номера."""
        status = '200'
        response_correct = ''.join(self.data_valid_text[:-10] + "9397777777")
        self.data_user['phone'] = 939_777_77_77
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_correct in response.text)

    def test_address_empty(self) -> None:
        """Негативный тест. Проверка адреса с применением пустой строки."""
        status: str = '400'
        response_not_correct: str = self.address_empty_text
        self.data_user['address'] = ''
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_address_short_str(self) -> None:
        """Негативный тест. Проверка адреса с применением знаков пробела."""
        status: str = '400'
        response_not_correct: str = self.address_short_text
        self.data_user['address'] = '  '
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_name_empty(self) -> None:
        """Негативный тест. Проверка адреса с отсутствием значений."""
        status: str = '400'
        response_not_correct: str = self.name_empty_text
        self.data_user.pop('name')
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_name_valid(self) -> None:
        """Позитивный тест. Проверка применения значений имени."""
        status: str = '200'
        response_correct: str = self.data_valid_text
        self.data_user['name'] = "Bazil"
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_correct in response.text)

    def test_index_empty(self) -> None:
        """Негативный тест. Проверка индекса с отсутствием значений."""
        status: str = '400'
        response_not_correct: str = self.index_empty_text
        self.data_user.pop('index')
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_index_invalid_str(self) -> None:
        """Негативный тест. Проверка индекса с текстовым значением."""
        status: str = '400'
        response_not_correct: str = self.index_invalid
        self.data_user['index'] = 'index of home'
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_index_invalid_length(self) -> None:
        """Негативный тест. Проверка индекса с применением избыточных символов в строке."""
        status: str = '400'
        response_not_correct: str = self.index_invalid
        self.data_user['index'] = "6543212661111"
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_not_correct in response.text)

    def test_index_valid(self) -> None:
        """Положительный тест. Проверка индекса с применением корректного значения."""
        status: str = '200'
        response_correct: str = self.data_valid_text
        self.data_user['index'] = 654321
        response = self.app.post(self.base_url, data=self.data_user)
        self.assertTrue(status in response.status)
        self.assertTrue(response_correct in response.text)


if __name__ == '__main__':
    unittest.main()
