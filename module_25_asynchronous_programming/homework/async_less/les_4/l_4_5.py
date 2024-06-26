# Использование as_completed

import asyncio
from aiohttp import ClientSession

from module_25_asynchronous_programming.homework.async_less.util import async_timed, fetch_status


@async_timed()
async def main():
    async with ClientSession() as client:
        statuses = [
            fetch_status(client=client, url="https://example.com", delay=1),
            fetch_status(client=client, url="https://example.com", delay=5),
            fetch_status(client=client, url="https://example.com", delay=3),
        ]

        for finished_task in asyncio.as_completed(statuses):
            print(await finished_task)
"""
Это дает нам дополнительное время для обработки результата первой успешно завершившейся сопрограммы,
пока остальные еще выполняются, поэтому приложение оказывается более отзывчивым.
Эта функция также дает больше контроля над обработкой исключений. Если задача возбудит исключение, 
то мы сможем обработать ее сразу же, поскольку оно возникает в точке, где мы ожидаем будущего объекта с помощью await.
"""

if __name__ == '__main__':
    asyncio.run(main())
