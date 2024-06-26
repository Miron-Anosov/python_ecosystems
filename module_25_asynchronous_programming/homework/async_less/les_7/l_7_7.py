import requests
import asyncio
from module_25_asynchronous_programming.homework.async_less.util import async_timed


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    urls = ['https://www.example.com' for _ in range(1000)]
    tasks = [asyncio.to_thread(get_status_code, url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())

"""
В версии Python 3.9 появилась сопрограмма asyncio.to_thread, которая еще больше упрощает передачу работы исполнителю 
пула потоков по умолчанию. Она принимает функцию, подлежащую выполнению в потоке, и её аргументы. Раньше для передачи 
аргументов нужно было использовать функцию functools.partial, так что теперь код стал немного чище. Затем эта функция 
выполняется с переданными аргументами в исполнителе по умолчанию и текущем цикле событий. Это позволяет еще 
упростить код. Сопрограмма to_thread устраняет необходимость в functools.partial и asyncio.get_running_loop, 
что уменьшает число строк кода.
"""