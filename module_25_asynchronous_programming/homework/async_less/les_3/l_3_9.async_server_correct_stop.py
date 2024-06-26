# Листинг 3.9 Добавление обработчика сигнала, снимающего все задачи

import asyncio
import signal
from asyncio import AbstractEventLoop
from typing import Set
from module_25_asynchronous_programming.homework.async_less.util import delay


def cansel_task():
    print('Получен сигнал SIGINT')
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f'Снимается {len(tasks)} задач')
    [task.cancel() for task in tasks]


async def main():
    loop: AbstractEventLoop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, cansel_task)

    await delay(10)

if __name__ == '__main__':
    asyncio.run(main())
