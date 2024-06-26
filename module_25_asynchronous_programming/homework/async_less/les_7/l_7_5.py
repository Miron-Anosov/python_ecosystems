import functools
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from module_25_asynchronous_programming.homework.async_less.util import async_timed


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(32) as pool:  # имеем возможность управлять кол-вом потоков.
        urls = ['https://www.example.com' for _ in range(1000)]
        tasks = [loop.run_in_executor(pool, functools.partial(get_status_code, url)) for url in urls]
        await asyncio.gather(*tasks)


asyncio.run(main())

"""
Мы создаем пул потоков, как и раньше, но вместо использования map строим список задач, вызывая функцию get_status_code 
из loop.run_in_executor. Получив список задач, мы можем ждать их завершения с помощью asyncio.gather или любой другой 
из уже знакомых нам функций asyncio. Под капотом loop.run_in_executor вызывает метод submit исполнителя пула потоков. 
Это ставит все переданные задачи в очередь. Затем рабочие потоки в пуле могут выбирать задачи из очереди и выполнять их 
до завершения. Этот подход не дает никакого выигрыша по сравнению с использованием пула потоков без asyncio, но, пока 
мы ждем await asyncio.gather, может выполняться другой код.
"""
