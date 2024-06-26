# Отправка веб-запроса с помощью aiohttp
import asyncio

from aiohttp import ClientSession

from module_25_asynchronous_programming.homework.async_less.util import async_timed


@async_timed()
async def fetch_status(client: ClientSession, url: str) -> int:
    async with client.get(url) as response:
        return response.status


@async_timed()
async def main():
    url = 'https://example.com'
    async with ClientSession() as session:
        status_code = await fetch_status(client=session, url=url)
        print(f"{url=}\n{status_code=}")


if __name__ == '__main__':
    asyncio.run(main())
