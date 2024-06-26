"""
1. Сконфигурируйте логгер программы из темы les_4 так, чтобы он:

* писал логи в файл stderr.txt;
* не писал дату, но писал время в формате HH:MM:SS,
  где HH — часы, MM — минуты, SS — секунды с ведущими нулями.
  Например, 16:00:09;
* выводил логи уровня INFO и выше.

2. К нам пришли сотрудники отдела безопасности и сказали, что, согласно новым стандартам безопасности,
хорошим паролем считается такой пароль, который не содержит в себе слов английского языка,
так что нужно доработать программу из предыдущей задачи.

Напишите функцию is_strong_password, которая принимает на вход пароль в виде строки,
а возвращает булево значение, которое показывает, является ли пароль хорошим по новым стандартам безопасности.
"""

import getpass
import hashlib
import logging.config
import os.path
import re
from logging import Formatter, FileHandler, StreamHandler
from typing import List
import requests

logger = logging.getLogger("password_checker")
file: str = os.path.abspath(os.path.join('stderr.txt'))
# формат сообщений для файлов
forma_file: Formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s ', datefmt='%H:%M:%S')
# формат сообщений для терминала
forma_terminal: Formatter = logging.Formatter(fmt='%(message)s')

logger.setLevel(level=logging.DEBUG)
# поток в файл
file_handler: FileHandler = logging.FileHandler(filename=file, mode='w', encoding='utf-8')
file_handler.setFormatter(fmt=forma_file)
file_handler.setLevel(level=logging.DEBUG)
# поток в терминал
console_handler: StreamHandler = logging.StreamHandler()
console_handler.setFormatter(fmt=forma_terminal)
console_handler.setLevel(level=logging.INFO)
# потоки передаются в handler
logger.addHandler(hdlr=file_handler)
logger.addHandler(hdlr=console_handler)


def check_words_list() -> set[str]:
    path: str = os.path.abspath(os.path.join('words_from_4_symbols.txt'))
    if not os.path.exists(path=path):
        url: str = 'https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words'

        with requests.get(url=url) as page:
            text: List[str] = page.text.split()
            words_from_4len: set = set(i for i in text if len(i) > 4)
        with open(file=path, mode='w', encoding='UTF-8') as file_new:
            file_new.write(' '.join(map(str, words_from_4len)))
        return words_from_4len
    else:
        with open(file=path, mode='r', encoding='UTF-8') as file_read:
            words_from_file: set = set(file_read.read().split())
        return words_from_file


words: set = check_words_list()


def is_strong_password(password: str) -> bool:
    if len(password) < 5:
        return True
    pattern: str = r'\b\w+\b'
    list_pattern: List[str] = re.findall(pattern, password)
    for pass_key in list_pattern:
        if pass_key in words:
            return True
    return False


def input_and_check_password() -> bool:
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass().lower()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False
    elif is_strong_password(password):
        logger.warning("Вы ввели слишком слабый пароль")
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")

    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
