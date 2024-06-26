# Неправильное использование блокирующего API как сопрограммы

import requests
import asyncio
from util import async_timed


@async_timed()
async def get_status() -> int:
    return requests.get('http://www.emample.com').status_code


@async_timed()
async def main():
    task_1 = asyncio.create_task(get_status())
    task_2 = asyncio.create_task(get_status())
    task_3 = asyncio.create_task(get_status())
    await task_1
    await task_2
    await task_3

if __name__ == '__main__':
    asyncio.run(main())
