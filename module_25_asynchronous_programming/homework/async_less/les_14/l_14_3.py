# Листинг 14.3 Принудительный запуск итерации цикла событий

import asyncio
from module_25_asynchronous_programming.homework.async_less.util import delay


async def create_tasks_no_sleep():
    task1 = asyncio.create_task(delay(5))
    task2 = asyncio.create_task(delay(10))
    print('К задачам применяется gather:')
    await asyncio.gather(task1, task2)


async def create_tasks_sleep():
    task1 = asyncio.create_task(delay(5))
    await asyncio.sleep(0)
    task2 = asyncio.create_task(delay(10))
    await asyncio.sleep(0)
    print('К задачам применяется gather:')
    await asyncio.gather(task1, task2)


async def main():
    print('--- Без asyncio.sleep(0) ---')
    await create_tasks_no_sleep()
    print('--- С asyncio.sleep(0) ---')
    await create_tasks_sleep()

asyncio.run(main())

"""
Сначала мы создаем обе задачи и вызываем для них `gather`, не используя `asyncio.sleep(0)`; 
все работает как обычно — сопрограммы `delay` не вызываются, пока не будет выполнено предложение `gather`. 
Затем мы вставляем `asyncio.sleep(0)` после создания каждой задачи. Теперь сообщения от сопрограммы `delay` 
печатаются немедленно, еще до вызова `gather`. Вызов `sleep` принудительно запускает следующую итерацию цикла событий,
что выливается в немедленное выполнение задачи.
"""