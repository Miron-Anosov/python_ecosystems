import asyncio
import datetime
import json
from pathlib import Path
from typing import Set, List, Iterable

import aiofiles
from aiohttp import ClientSession, ClientTimeout, ServerTimeoutError, ClientConnectorError, ClientOSError
from bs4 import BeautifulSoup
from bs4 import Tag
from yarl import URL

from sum_links_from_json_file import count_links

OUT_PATH = Path(__file__).parent
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()
FILE_PATH = OUT_PATH / f'links_{datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S")}.json'

sem = asyncio.Semaphore(250)


async def crawl_url(session: ClientSession, url: str, researched_links: Set[str], deep: int = 3, ) -> Set:
    """Обходим рекурсивно все ссылки"""
    external_links: Set[str] = set(url)

    if not deep:
        return external_links

    try:
        async with sem:
            async with session.get(url) as resource:
                researched_links.add(url)
                if resource.status != 200:
                    return set()

                result: bytes = await resource.read()

                loop = asyncio.get_running_loop()
                links = await loop.run_in_executor(None, parsing_links,
                                                   result)

                tasks: List = []
                for link in links:
                    if link not in researched_links:  # избегаем создание таски, которая уже обрабатывалась.
                        task = asyncio.create_task(crawl_url(session, link, researched_links, deep - 1))
                        tasks.append(task)

                if tasks:

                    results: Iterable[Set[str]] = await asyncio.gather(*tasks, return_exceptions=True)

                    for set_links in results:  # Извлечение ссылок при раскрутке стека вызовов.
                        if isinstance(set_links, set):
                            external_links.update(set_links)

                return external_links

    except (ServerTimeoutError, ClientConnectorError, ClientOSError, asyncio.TimeoutError, OSError,):
        return external_links

    finally:
        await writer(data=list(external_links))


async def writer(data: List[str]):
    """Запись готовых ссылок в файл"""
    async with aiofiles.open(FILE_PATH, 'w+') as file:
        await file.write(json.dumps(data))


def parsing_links(data: bytes) -> Iterable[str]:
    """Извлекаются данные из тега и сохраняют во множество, что бы сразу исключить повторяющиеся ссылки и отдаем
    в качестве итерируемого объекта из генератора, который извлекает ссылки"""
    soup = BeautifulSoup(data, 'lxml')
    all_links: Set[Tag] = set(soup.find_all('a', href=True))
    for link in select_extra_links(all_links):
        yield normalize_url(link)


def select_extra_links(links: set[Tag]) -> Iterable[str]:
    """Извлекаются внешние ссылки (начинающиеся с http:// или https://)"""
    for link in links:
        if link['href'].startswith(('http://', 'https://')):
            yield link['href']


def normalize_url(url: str) -> str:
    """Нормализация ссылок"""
    parsed_url = URL(url)
    normalized_url = parsed_url.with_scheme(parsed_url.scheme.lower()).with_host(parsed_url.host.lower())

    # Удаление стандартных портов
    if (parsed_url.scheme == 'http' and parsed_url.port == 80) or (
            parsed_url.scheme == 'https' and parsed_url.port == 443):
        normalized_url = normalized_url.with_port(None)

    return str(normalized_url)


async def create_session(start_url: str):
    """Создается сессия и запускается рекурсивный обход"""
    researched_links: Set[str] = set()
    async with ClientSession(timeout=ClientTimeout(connect=5, total=10)) as session:
        return await crawl_url(session=session, url=start_url, researched_links=researched_links)


def main():
    result = asyncio.run(create_session('http://habr.com'))
    print(f'кол-во собранных ссылок: {len(result)}')


if __name__ == '__main__':
    main()
    sum_links = count_links(FILE_PATH)
    print('Ссылок в файле', sum_links)
