# Попытка конкурентного выполнения счетного кода. Код будет выполнен последовательно
import asyncio
from util.time_decorator import async_timed


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
    await task_one
    await task_two

if __name__ == '__main__':
    asyncio.run(main())
