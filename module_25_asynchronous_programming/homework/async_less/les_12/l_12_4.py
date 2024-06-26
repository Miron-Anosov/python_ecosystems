# Листинг 12.4 Робот с очередью
import asyncio
import aiohttp
import logging
from asyncio import Queue
from aiohttp import ClientSession
from bs4 import BeautifulSoup


class WorkItem:
    def __init__(self, item_depth: int, url: str):
        self.item_depth = item_depth
        self.url = url


async def worker(worker_id: int, queue: Queue, session: ClientSession, max_depth: int):
    print(f'Исполнитель {worker_id}')
    while True:  # Выбрать из очереди URL-адрес и начать его скачивание
        work_item: WorkItem = await queue.get()
        print(f'Исполнитель {worker_id}: обрабатывается {work_item.url}')
        await process_page(work_item, queue, session, max_depth)
        print(f'Исполнитель {worker_id}: закончена обработка {work_item.url}')
        queue.task_done()


async def process_page(work_item: WorkItem, queue: Queue, session: ClientSession, max_depth: int):
    """Скачиваем страницу, находим в ней все ссылки и отправляем их в очередь."""
    try:
        response = await asyncio.wait_for(session.get(work_item.url), timeout=3)
        if work_item.item_depth == max_depth:
            print(f'Макс глубина достигнута '
                  f'для {work_item.url}')
        else:
            body = await response.text()
            soup = BeautifulSoup(body, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                queue.put_nowait(WorkItem(work_item.item_depth + 1,
                                          link['href']))
    except Exception as e:
        logging.exception(f'Error processing url {work_item.url}')


async def main():
    """Создать очередь и 100 задач-исполнителей
    для обработки URL-адресов"""
    start_url = 'http://example.com'
    url_queue = Queue()
    url_queue.put_nowait(WorkItem(0, start_url))
    async with aiohttp.ClientSession() as session:
        workers = [asyncio.create_task(worker(i, url_queue, session, 3))
                   for i in range(100)]
        await url_queue.join()
        [w.cancel() for w in workers]


asyncio.run(main())
