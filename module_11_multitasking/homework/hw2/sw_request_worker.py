import logging
import threading
import time
from typing import Callable
from functools import wraps

from request_func import star_wars_request
from db_manager import sqlite_manager as db

logger: logging = logging.getLogger(__name__)

__all__ = ['major_thread', 'ather_threads']


def timer(func: Callable) -> Callable:
    """
    Декоратор-таймер. Обрабатывает затраченное время на выполнение энных операций.
    Args:
        func: Callable
    Returns:
        func: Callable
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        start_request: float = time.time()
        result = func(*args, **kwargs)
        finish: float = time.time() - start_request
        logger.info(f'Spent time for {func.__name__}: {finish:.3f}')
        return result

    return wrapper


def response_threads(name_db: str, queue_characters: int) -> None:
    """
    Функция обрабатывает запросы api: https://swapi.dev/api/. Передает их значения в БД.
    Args:
        name_db: str:  Название БД.
        queue_characters: int: Стартовая позиция очереди запросов к api.

    Returns:
        None
    """
    control_requests: int = 5
    with db(name_db=name_db) as base:
        while control_requests:
            logger.debug(f'Create request №{queue_characters}')
            character: tuple[str, str, str] = star_wars_request(queue_characters)
            if character:
                name, age, gender = character
                base.insert_new_actor(name=name, age=age, gender=gender)
                return
            else:
                control_requests -= 1
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
    completed: int = 0

    with db(name_db=name_db) as base:
        while True:
            logger.debug(f'Create request №{queue_characters}')
            character: tuple[str, str, str] = star_wars_request(queue_characters)

            if character:
                name, age, gender = character
                base.insert_new_actor(name=name, age=age, gender=gender)
                completed += 1
                queue_characters += 1
            else:
                queue_characters += 1

            if completed == 20:
                break


@timer
def ather_threads(name_db: str) -> None:
    """
    Запускает 20 запросов в разных потоках, которые в свою очередь обращаются к api: https://swapi.dev/api/.
    Передает их значения в БД.
    Args:
        name_db: str: Название БД.
    Returns:
        None
    """

    other_treads = [threading.Thread(target=response_threads,
                                     kwargs={'name_db': name_db, 'queue_characters': i}) for i in range(1, 21)]

    for tread in other_treads:
        tread.start()

    for tread in other_treads:
        tread.join()
