import unittest
from typing import List

from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    """ Тесты отрабатывают исключения с контекстным менеджером BlockError."""

    def test_ZeroDivisionError(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            err_types: set = {TypeError}
            with BlockErrors(err_types):
                a = 1 / 0
            print('Выполнено без ошибок')

    def test_TypeError(self) -> None:
        with self.assertRaises(TypeError):
            err_types: set = {ZeroDivisionError}
            with BlockErrors(err_types):
                a = 1 / '0'
            print('Выполнено без ошибок')

    def test_TypeError2(self) -> None:
        with self.assertRaises(TypeError):
            outer_err_types: dict = {}
            with BlockErrors(outer_err_types):
                inner_err_types: set = {ZeroDivisionError}
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
                print('Внутренний блок: выполнено без ошибок')
            print('Внешний блок: выполнено без ошибок')

    def test_Exception(self) -> None:
        with self.assertRaises(Exception):
            err_types: set = {}
            with BlockErrors(err_types):
                a = 1 / '0'
            print('Выполнено без ошибок')

    def test_indexError(self) -> None:
        list_num: List[int] = [1, 2, 3, 4, 56, ]
        with self.assertRaises(IndexError):
            err_types: set = {ValueError}
            with BlockErrors(err_types):
                x = list_num[5]
            print('Выполнено без ошибок')

    def test_ValueError(self) -> None:
        list_num: List[int] = [1, 2, 3, 4, 56, ]
        with self.assertRaises(ValueError):
            err_types: set = {IndexError}
            with BlockErrors(err_types):
                x = list_num.index(7)
            print('Выполнено без ошибок')

    def test_KeyError(self) -> None:
        dict_num: dict = {}
        with self.assertRaises(KeyError):
            err_types: set = {IndexError}
            with BlockErrors(err_types):
                x = dict_num.pop('err')
            print('Выполнено без ошибок')

    def test_ImportError(self) -> None:
        with self.assertRaises(ImportError):
            err_types: set = {KeyError}
            with BlockErrors(err_types):
                dict_num: dict = {'err': 3}
                x = dict_num.pop('err')
                with BlockErrors(err_types):
                    import icecream
                print('Выполнено без ошибок_1')

            print('Выполнено без ошибок_2')

    def test_AttributeError(self) -> None:
        with self.assertRaises(AttributeError):
            err_types: set = {ImportError}
            with BlockErrors(err_types):
                err_types.next
            print('Выполнено без ошибок')

    def test_StopIteration(self) -> None:
        with self.assertRaises(StopIteration):
            err_types: set = {AttributeError}
            with BlockErrors(err_types):
                word = iter('word')
                next(word)
                next(word)
                next(word)
                next(word)
                next(word)
            print('Выполнено без ошибок')


if __name__ == '__main__':
    unittest.main()
