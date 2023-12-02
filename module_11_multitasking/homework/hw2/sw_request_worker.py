import logging
import threading
import time
from typing import Callable, List
from functools import wraps

from request_func import star_wars_request
from db_manager import sqlite_manager as db

logger: logging = logging.getLogger(__name__)

__all__ = ['major_thread', 'twenty_threads']


def timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_request: float = time.time()
        result = func(*args, **kwargs)
        finish: float = time.time() - start_request
        logger.info(f'Spent time for {func.__name__}: {finish:.3f}')
        return result

    return wrapper


def sqlite3_db(data_characters: List[tuple[str, str, str]], name_db: str) -> None:
    """
    Функция записывает данные об персонажах в базу данных.
    Args:
        name_db: str: Название БД.
        data_characters:List:
            name: Имя персонажа.
            age: Возраст персонажа.
            gender: Пол персонажа.
            name_db: Название БД.

    Returns:
        None
    """
    with db(name_db=name_db) as base:
        for name, age, gender in data_characters:
            base.insert_new_actor(name=name, age=age, gender=gender)


def response_threads(data_db: List, queue_characters: int) -> None:
    """
    Функция обрабатывает запросы api: https://swapi.dev/api/. Передает их значения в БД.
    Args:
        data_db: str: Данные для записи в БД.
        queue_characters: int: Стартовая позиция очереди запросов к api.

    Returns:
        None
    """

    while queue_characters:
        logger.debug(f'Create request №{queue_characters}')
        character: tuple[str, str, str] = star_wars_request(queue_characters)
        if character:
            data_db.append(character)
            return
        else:
            queue_characters += 1


@timer
def major_thread(name_db: str) -> None:
    """
    Функция обрабатывает запросы api передает их значения в БД.
    Args:
        name_db: str: Название БД.

    Returns:
        None
    """
    queue_characters: int = 1
    completed = 0
    data_requests: list[tuple] = []
    while True:
        logger.debug(f'Create request №{queue_characters}')
        character: tuple[str, str, str] = star_wars_request(queue_characters)

        if character:
            data_requests.append(character)
            completed += 1
            queue_characters += 1
        else:
            queue_characters += 1

        if completed == 20:
            sqlite3_db(data_requests, name_db=name_db)
            break


@timer
def twenty_threads(name_db: str) -> None:
    """
    Запускает 20 threads, которые в свою очередь обращаются к api: https://swapi.dev/api/.
    Передает их значения в БД.
    Returns:
        None
    """

    data_requests: list[tuple] = []
    second_treads = [threading.Thread(target=response_threads,
                                      kwargs={'data_db': data_requests, 'queue_characters': i}) for i in range(1, 21)]

    for tread in second_treads:
        tread.start()
    for tread in second_treads:
        tread.join()

    sqlite3_db(data_characters=data_requests, name_db=name_db)
