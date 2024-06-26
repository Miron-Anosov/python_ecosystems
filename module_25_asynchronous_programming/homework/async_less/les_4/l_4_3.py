# Применение timeout

import asyncio

from aiohttp import ClientSession, ClientTimeout

from module_25_asynchronous_programming.homework.async_less.util import async_timed


@async_timed()
async def fetch_status(client: ClientSession, url: str) -> int:
    ten_millis = ClientTimeout(total=0.8)
    async with client.get(url, timeout=ten_millis) as response:
        return response.status


@async_timed()
async def main():
    url = 'https://example.com'
    timeout = ClientTimeout(total=1, connect=0.1)
    try:
        async with ClientSession(timeout=timeout) as session:
            status_code = await fetch_status(client=session, url=url)
            print(f"{url=}\n{status_code=}")
    except asyncio.TimeoutError:
        print('Ошибка соединения.')

if __name__ == '__main__':
    asyncio.run(main())
