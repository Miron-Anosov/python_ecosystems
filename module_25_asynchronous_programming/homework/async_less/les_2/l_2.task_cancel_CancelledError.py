# Снятие задачи
import asyncio
from asyncio import CancelledError
from util.delayfunctions import delay


async def long_task():
    task = asyncio.create_task(delay(10))
    seconds = 0
    while not task.done():
        print(f'Выполняется задача в течении {seconds}')
        await asyncio.sleep(1)
        seconds += 1
        if seconds == 5:
            task.cancel()
    try:
        await task
    except CancelledError:
        print('Задача не выполнена')


if __name__ == '__main__':
    asyncio.run(long_task())
