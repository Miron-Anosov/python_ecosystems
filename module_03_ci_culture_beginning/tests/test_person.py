import unittest
from typing import Optional, TypeVar

from module_03_ci_culture_beginning.homework.hw4.person import Person

T = TypeVar('T')


class TestPerson(unittest.TestCase):
    def setUp(self):
        """
        Настройка тестового окружения перед запуском каждого теста.
        """
        self.person: T = Person(name='Tom', year_of_birth=2000)

    def test_get_name(self):
        """
        Тест метода get_name(). Проверяет истинное значение.
        """
        true_name: str = 'Tom'
        name: str = self.person.get_name()
        self.assertEqual(true_name, name)

    def test_get_name_false(self):
        """
        Тест метода get_name(). Проверяет ошибочное значение.
        """
        true_name: str = 'Тоm'  # Кириллица
        name: str = self.person.get_name()
        self.assertFalse(true_name == name)

    def test_set_name(self):
        """
        Тест метода set_name(). Проверяет истинные значения.
        """
        true_name: str = 'Max'
        self.person.set_name('Max')
        name: str = self.person.get_name()
        self.assertTrue(true_name == name)

    def test_get_age(self):
        """
        Текст метода get_age(). Проверяет равенство значения возраста.
        """
        yob_true: int = 23
        yob: int = abs(self.person.get_age())
        self.assertEqual(yob_true, yob)

    def test_set_address(self):
        """
        Текст метода set_address(). Проверяет значения адресов, когда в адресе имеются данные.
        """
        new_address: str = 'Почтовая 1'
        self.person.set_address(new_address)
        address: str = self.person.get_address()
        self.assertTrue(new_address == address)

    def test_get_address(self):
        """
        Текст метода get_address(). Проверяет значения адресов, когда в адресе None.
        """
        true_address: Optional[bool] = None
        address: str = self.person.get_address()
        self.assertIs(true_address, address)

    def test_is_homeless_true(self):
        """
        Текст метода is_homeless(). Проверяет значения адресов, когда в адресе не имеются данные.
        """
        flag: bool = True
        real_flag: bool = self.person.is_homeless()
        self.assertIs(flag, real_flag)

    def test_is_homeless_false(self):
        """
        Текст метода is_homeless(). Проверяет значения адресов, когда в адресе имеются данные.
        """
        flag: bool = False
        new_address: str = 'Почтовая 1'
        self.person.set_address(new_address)
        real_flag: bool = self.person.is_homeless()
        self.assertIs(flag, real_flag)


if __name__ == '__main__':
    unittest.main()
