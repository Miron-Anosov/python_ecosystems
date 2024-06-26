import asyncio
from asyncio import Condition
import random


class TaskQueue:
    def __init__(self):
        self.condition = Condition()
        self.queue = []

    async def add_task(self, task):
        async with self.condition:
            self.queue.append(task)
            print(f"Добавлена задача: {task}")
            self.condition.notify()  # Уведомляем одного потребителя

    async def get_task(self):
        async with self.condition:
            while not self.queue:
                print("Потребитель ожидает задачу...")
                await self.condition.wait()
            return self.queue.pop(0)


async def producer(queue):
    for i in range(1, 11):
        task = f"Задача {i}"
        await queue.add_task(task)
        await asyncio.sleep(random.uniform(0.5, 2))


async def consumer(queue, name):
    while True:
        task = await queue.get_task()
        print(f"{name} обрабатывает {task}")
        await asyncio.sleep(random.uniform(1, 3))  # Имитация обработки


async def main():
    queue = TaskQueue()

    # Создаем задачи для продюсера и потребителей
    producer_task = asyncio.create_task(producer(queue))
    consumer_tasks = [
        asyncio.create_task(consumer(queue, f"Потребитель {i}"))
        for i in range(3)
    ]

    # Ждем завершения продюсера
    await producer_task

    # Даем потребителям время на завершение оставшихся задач
    await asyncio.sleep(5)

    # Отменяем задачи потребителей
    for task in consumer_tasks:
        task.cancel()

    # Ждем завершения всех задач
    await asyncio.gather(*consumer_tasks, return_exceptions=True)


asyncio.run(main())
