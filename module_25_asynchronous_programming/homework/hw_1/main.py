import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import aiohttp

# import aiofiles

URL = 'https://cataas.com/cat'
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


async def get_cat(client: aiohttp.ClientSession, loop: AbstractEventLoop, sem: asyncio.Semaphore,
                  thread: ThreadPoolExecutor,
                  idx: int) -> None:
    async with sem:
        async with client.get(URL) as response:
            result = await response.read()
            await loop.run_in_executor(thread, write_to_disk, result, idx)


def write_to_disk(content: bytes, id_: int) -> None:
    file_path = OUT_PATH / f'{id_}.png'
    with open(file_path, mode='wb') as f:
        f.write(content)


async def get_all_cats(threads_pool: ThreadPoolExecutor, loop: AbstractEventLoop, cats):
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30)) as client:
        tasks = [get_cat(client, loop, sem, threads_pool, i) for i in range(cats)]
        return await asyncio.gather(*tasks)


async def run(cats):
    """asyncio.to_thread можно так же применить"""
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(32) as threads_pool:
        return await get_all_cats(threads_pool, loop, cats)


def async_cats(cats=10):
    asyncio.run(run(cats))


if __name__ == '__main__':
    async_cats()
