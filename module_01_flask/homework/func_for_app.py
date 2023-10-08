import os
import re
from random import choice
from typing import List, TypeVar

T = TypeVar('T')


class Counter:
    """
    Класс ведет счет запроса страницы.
    Attributes:
        cls.___sing: None | Counter : Атрибут отвечает за использование одного объекта данного класса.
        cls.__count: int : Атрибут используется  для ведения счета при вызове данного объекта.
    """
    __sing = None
    __count = 0

    def __new__(cls, *args, **kwargs) -> T:
        """Создаем Singleton"""
        if cls.__sing is None:
            cls.__sing = super(Counter, cls).__new__(cls)
        cls.__count += 1
        return cls.__sing

    def __str__(self):
        """
        Метод выводит результат использования данного класса.
        """
        return f'{self.__count}'


def counter_func() -> T:
    """Функция предназначения для подсчета статистических данных-отвечает за ведение счета использования страницы.
    Returns: T(Counter)
    """
    return Counter()


def word_from_book() -> str:
    """
    Функция возвращает случайное слово из книги.
    Returns: str
    """
    pattern = r'\b(\w+)\b'  # Экранируем слова \b
    path = os.path.abspath(os.path.join('war_and_peace.txt'))
    list_word: List[str] = []
    if not list_word:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                words = re.findall(pattern, line)
                list_word.extend(words)
        return choice(list_word)
    else:
        return choice(list_word)


def car_output() -> str:
    """
    Функция возвращает список автомобилей. Так же можно изменить актуальные данные.
    Returns: str
    """
    car_list: List[str] = ["Chevrolet", "Renault", "Ford", "Lada"]
    car = ''.join(f'{car}, ' for car in car_list)
    return car


def cat_random_output() -> str:
    """
    Функция возвращает случайную кошку.
    Returns: str
    """
    cats_list: List[str] = ["корниш-рекс,", "русская голубая", "шотландская", "вислоухая", "мейн-кун", "манчкин"]
    cat = choice(cats_list)
    return cat
