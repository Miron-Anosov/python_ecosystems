"""
1. Сконфигурируйте логгер программы из темы 4 так, чтобы он:

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

url = 'https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words'

with requests.get(url) as page:
    text: List[str] = page.text.split()
    words: set = set(i for i in text if len(i) > 4)


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
    terminal_handler: StreamHandler = logging.StreamHandler()
    terminal_handler.setFormatter(fmt=forma_terminal)
    terminal_handler.setLevel(level=logging.INFO)
    # потоки передаются в handler
    logger.addHandler(hdlr=file_handler)
    logger.addHandler(hdlr=terminal_handler)

    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")

    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
