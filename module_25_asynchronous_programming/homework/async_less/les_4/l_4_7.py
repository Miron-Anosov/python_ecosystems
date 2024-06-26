# Изучения поведения wait по умолчанию


import asyncio
from aiohttp import ClientSession

from module_25_asynchronous_programming.homework.async_less.util import async_timed, fetch_status


@async_timed()
async def main():
    async with ClientSession() as client:
        statuses = [
            asyncio.create_task(fetch_status(client=client, url="https://example.com", )),
            asyncio.create_task(fetch_status(client=client, url="https://example.com", )),
        ]

        done, pending = await asyncio.wait(statuses)

        print(f'Число завершенных задач: {len(done)}')
        print(f'Число не завершенных задач: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)

if __name__ == '__main__':
    asyncio.run(main())
