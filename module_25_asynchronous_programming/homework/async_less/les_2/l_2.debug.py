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
    loop = asyncio.get_running_loop()
    loop.slow_callback_duration = 0.250
    task = loop.create_task(cpu_long_worker())
    await task

if __name__ == '__main__':
    asyncio.run(main(), debug=True)
