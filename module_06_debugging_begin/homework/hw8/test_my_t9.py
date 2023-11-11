import unittest
from typing import List

from my_t9 import my_t9


class TestT9(unittest.TestCase):

    def test_basement(self):
        """
        Тест проверяет соответствие цифрового значения '22736368' с буквенным 'basement'.
        """
        nums: str = '22736368'
        result: List[str] = my_t9(input_numbers=nums)
        print(result)
        self.assertTrue('basement' in result)

    def test_negative(self):
        """
        Тест проверяет не соответствие цифрового значения ''2637422' с буквенным 'basement'.
        """
        nums: str = '2637422'
        result: List[str] = my_t9(input_numbers=nums)
        print(result)
        self.assertFalse('basement' in result)

    def test_hello(self):
        """
        Тест проверяет соответствие цифрового значения '43556' с буквенным 'hello'.
        """
        nums: str = '43556'
        result: List[str] = my_t9(input_numbers=nums)
        print(result)
        self.assertTrue('hello' in result)

    def test_world(self):
        """
        Тест проверяет соответствие цифрового значения '96753' с буквенным 'world'.
        """
        nums: str = '96753'
        result: List[str] = my_t9(input_numbers=nums)
        print(result)
        self.assertTrue('world' in result)

    def test_hello_world(self):
        """
        Тест проверяет соответствие цифрового значения '43556' и '96753' с буквенным 'hello world'.
        """
        nums: str = '43556'
        result: List[str] = my_t9(input_numbers=nums)
        nums_2: str = '96753'
        result_2: List[str] = my_t9(input_numbers=nums_2)
        result.extend(result_2)
        str_result = ' '.join(i for i in result)
        print(str_result)
        self.assertTrue('hello world' in str_result)

    def test_raise(self):
        """
        Текс проверяет вызов исключения ValueError.
        """
        nums: str = '43556e'
        with self.assertRaises(ValueError):
            my_t9(nums)


if __name__ == '__main__':
    unittest.main()
