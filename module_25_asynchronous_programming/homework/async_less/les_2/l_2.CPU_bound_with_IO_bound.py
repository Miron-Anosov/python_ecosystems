# Попытка конкурентного выполнения счетного кода.
# Код будет выполнен последовательно, хоть и присутствует асинхронная задача

import asyncio
from util import async_timed, delay


@async_timed()
async def cpu_long_worker() -> int:
    counter = 0
    for i in range(100_000_000):
        counter += i
    return counter


@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_long_worker())
    task_two = asyncio.create_task(cpu_long_worker())
    task_io = asyncio.create_task(delay(5))
    await task_io
    await task_one
    await task_two

if __name__ == '__main__':
    asyncio.run(main())
