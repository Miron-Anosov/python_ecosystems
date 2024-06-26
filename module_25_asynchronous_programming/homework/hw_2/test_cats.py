import asyncio
import time

from cats_proc import process_cats
from cats_threads import treads_cats
from module_25_asynchronous_programming.homework.hw_1.main import async_cats
from module_25_asynchronous_programming.materials.async_cats.main import main as async_cats_with_aiofiles


def create_cats(func):
    for cats in 10, 50, 100:
        start = time.time()
        if asyncio.iscoroutinefunction(func):
            asyncio.run(func(cats))
        else:
            func(cats)
        stop = time.time() - start
        print(f'{func.__name__} with {cats=} completed for {stop}')


def main():
    for func in process_cats, treads_cats, async_cats, async_cats_with_aiofiles:
        create_cats(func)
        print()


if __name__ == '__main__':
    main()
