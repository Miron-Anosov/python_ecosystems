# Использование таймера для as_completed

import asyncio
from aiohttp import ClientSession

from module_25_asynchronous_programming.homework.async_less.util import async_timed, fetch_status


@async_timed()
async def main():
    async with ClientSession() as client:
        statuses = [
            fetch_status(client=client, url="https://example.com", delay=1),
            fetch_status(client=client, url="https://example.com", delay=5),
            fetch_status(client=client, url="https://example.com", delay=3),
        ]

        for finished_task in asyncio.as_completed(statuses, timeout=4):
            try:
                result = await finished_task
                print(result)
            except asyncio.TimeoutError:
                print('Произошёл таймаут')

        for error_task in asyncio.all_tasks():
            print(error_task)

"""
as_completed справляется со своей задачей – возвращать результат по мере поступления, но она не лишена недостатков. 
Первый заключается в том, что хотя мы и получаем результаты в темпе их поступления, но невозможно сказать, 
какую сопрограмму или задачу мы ждем, поскольку порядок абсолютно не детерминирован. Если порядок нас не волнует, 
то и  ладно, но если требуется ассоциировать результаты с запросами, то возникает проблема.
Второй недостаток в том, что, хотя исключения по истечении тайм- аута возбуждаются как положено, 
все созданные задачи продолжают работать в  фоновом режиме. А  если мы захотим их снять, то будет трудно понять,
какие задачи еще работают. Вот вам и еще одна проблема! Если эти проблемы требуется решить, то нужно точно знать,
какие допускающие ожидание объекты уже завершились, а какие еще нет. Поэтому asyncio предоставляет функцию wait.
"""

if __name__ == '__main__':
    asyncio.run(main())
