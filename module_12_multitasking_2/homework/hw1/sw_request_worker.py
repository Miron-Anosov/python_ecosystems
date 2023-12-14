import logging
import time
from multiprocessing.pool import ThreadPool, Pool
from multiprocessing import cpu_count
from typing import Callable
from functools import wraps

from request_func import star_wars_request
from db_manager import sqlite_manager as db

logger: logging = logging.getLogger(__name__)


def timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        start_request: float = time.time()
        result = func(*args, **kwargs)
        finish: float = time.time() - start_request
        logger.info(f'Spent time for {func.__name__}: {finish:.3f}')
        return result

    return wrapper


def writing_db(name_db: str, character: tuple) -> None:
    if character:
        name, age, gender = character
        with db(name_db=name_db) as db_worker:
            db_worker.insert_new_actor(name=name, age=age, gender=gender)


@timer
def do_thread_pool() -> None:
    with ThreadPool(processes=cpu_count() * 10) as tp:
        async_result = tp.map_async(func=star_wars_request, iterable=range(1, 21))
        result = async_result.get()
        async_result.wait()
        [writing_db(name_db='sw_thread_pool', character=character) for character in result]


@timer
def do_only_pool() -> None:
    with Pool(processes=cpu_count()) as pool:
        async_result = pool.map_async(func=star_wars_request, iterable=range(1, 21))
        result = async_result.get()
        async_result.wait()
        [writing_db(name_db='sw_pool', character=character) for character in result]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    do_thread_pool()
    do_only_pool()
