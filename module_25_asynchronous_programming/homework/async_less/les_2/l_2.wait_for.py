# Снятие задачи по таймеру
import asyncio
from asyncio import TimeoutError
from util.delayfunctions import delay


async def long_task():
    task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(task, 1)
        print(result)
    except TimeoutError:
        print(f'the task killed? {task.cancelled()}')


if __name__ == '__main__':
    asyncio.run(long_task())
