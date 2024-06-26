import functools
import requests
import asyncio
from module_25_asynchronous_programming.homework.async_less.util import async_timed


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    urls = ['https://www.example.com' for _ in range(1000)]
    # Не имеем возможность управлять кол-вом потоков. По умолчанию существует до входа в цикл событий.
    tasks = [loop.run_in_executor(None, functools.partial(get_status_code, url)) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)


asyncio.run(main())

"""
В документации по asyncio сказано, что параметр executor метода run_in_executor может быть равен None. В этом случае 
используется исполнитель по умолчанию, ассоциированный с циклом событий. Можно считать, что это допускающий повторное 
использование синглтонный исполнитель для всего приложения. Исполнитель по умолчанию всегда имеет тип 
ThreadPoolExecutor, если с помощью метода loop.set_default_executor не было задано иное. Следовательно, мы можем 
упростить код в листинге 7.5, как показано ниже.
"""