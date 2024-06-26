# Листинг 12.10 LIFO-очередь
import asyncio
from asyncio import Queue, LifoQueue
from dataclasses import dataclass, field


@dataclass(order=True)
class WorkItem:
    priority: int
    order: int
    data: str = field(compare=False)


async def worker(queue: Queue):
    while not queue.empty():
        work_item: WorkItem = await queue.get()  # Выбрать элемент из очереди, или «вытолкнуть» его из стека
        print(f'Processing work item {work_item}')
        queue.task_done()


async def main():
    lifo_queue = LifoQueue()

    work_items = [WorkItem(3, 1, 'Lowest priority first'),
                  WorkItem(3, 2, 'Lowest priority second'),
                  WorkItem(3, 3, 'Lowest priority third'),
                  WorkItem(2, 4, 'Medium priority'),
                  WorkItem(1, 5, 'High priority')]

    worker_task = asyncio.create_task(worker(lifo_queue))

    for work in work_items:
        lifo_queue.put_nowait(work)  # Поместить элемент в очередь, или «затолкнуть» его в стек

    await asyncio.gather(lifo_queue.join(), worker_task)


asyncio.run(main())

"""Обратите внимание, что элементы обрабатываются в порядке, противоположном тому, в каком вставлялись. 
Поскольку это стек, то так и должно быть – ведь первым обрабатывается элемент, помещенный в очередь первым."""