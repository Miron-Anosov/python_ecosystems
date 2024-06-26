import asyncio

from aiohttp import ClientSession


async def fetch_status(client: ClientSession, url: str, delay: int = 0) -> int:
    if delay:
        print(f'Делаю что-то на протяжении {delay} sec.')
        await asyncio.sleep(delay)

    async with client.get(url) as response:
        return response.status
