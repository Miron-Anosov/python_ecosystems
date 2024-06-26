# Защита от снятия задачи по таймеру
import asyncio
from asyncio import TimeoutError
from util.delayfunctions import delay


async def long_task():
    task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except TimeoutError:
        print("Задача заняла более 5с, скорo oна закончится!")
        result = await task
        print(result)
        print(f'the task killed?: {task.cancelled()}')


if __name__ == '__main__':
    asyncio.run(long_task())
