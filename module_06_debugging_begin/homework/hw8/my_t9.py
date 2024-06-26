"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* les_4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
import os.path
from typing import List, Dict
import re
import requests


def check_word() -> str:
    path = os.path.abspath(os.path.join('words.txt'))
    if not os.path.exists(path=path):
        url = 'https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words'
        with requests.get(url) as page:
            words_list: List[str] = page.text.split()
            word_string: str = ' '.join(map(str, words_list))
        with open(path, 'w', encoding='UTF-8') as file:
            file.write(word_string)
        return word_string
    else:
        with open(path, 'r', encoding="UTF-8") as file:
            text: str = file.read()
        return text


words_string: str = check_word()


def generate_pattern(input_numbers: str) -> str:
    nums_table: Dict[str:str] = {'2': '[ABCabc]', '3': '[DEFdef]', 'les_4': '[GHIghi]', '5': '[JKLjkl]',
                                 '6': '[MNOmno]', '7': '[PQRSpqrs]', '8': '[TUVtuv]', '9': '[WXYZwxyz]'}
    pattern: str = r'\b'
    for collection_symbols in input_numbers:
        if nums_table.get(collection_symbols):
            pattern: str = ''.join(pattern + nums_table.get(collection_symbols))
    pattern: str = ''.join(pattern + r'\b')
    return pattern


def my_t9(input_numbers: str) -> List[str]:
    if input_numbers.isdigit():
        pattern: str = generate_pattern(input_numbers=input_numbers)
        collection_words: List[str] = list(set(re.findall(pattern=pattern, string=words_string)))
        return collection_words
    else:
        raise ValueError('Must be only digital')


if __name__ == '__main__':
    numbers: str = input('numbers:')
    words: List[str] = my_t9(numbers)
    print(*words, sep='\n')
