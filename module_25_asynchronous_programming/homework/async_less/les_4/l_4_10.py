#  Использование timeout в wait

import asyncio
import aiohttp

from module_25_asynchronous_programming.homework.async_less.util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as client:
        good_request = fetch_status(client=client, url="https://example.com")
        good_request_2 = fetch_status(client=client, url="https://example.com")
        good_request_long = fetch_status(client=client, url="https://example.com", delay=2)

        pending = [asyncio.create_task(good_request),
                   asyncio.create_task(good_request_2),
                   asyncio.create_task(good_request_long),
                   ]

        # asyncio.wait(return_when=ALL_COMPLETED) default
        done, pending = await asyncio.wait(pending, timeout=1)

        print(f'Число завершенных задач: {len(done)}')
        print(f'Число не завершенных задач: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)


""" 
Сопрограммы не снимаются
Если при выполнении сопрограммы, запущенной с  помощью wait_for, случался тайм-аут, то она автоматически снималась. 
В  случае wait это не так: поведение ближе к gather и as_completed. Если мы хотим снять сопрограммы из-за тайм-аута, 
то должны явно обойти их и снять каждую.

Исключения не возбуждаются
wait не возбуждает исключения в случае тайм-аута, в отличие от wait_ for и  as_completed. Когда случается тайм-аут, 
wait возвращает все за- вершившиеся задачи, а также те, что еще не завершились в момент таймаута.

Заметим, что, как и раньше, задачи в множестве pending не сняты и продолжают работать, несмотря на тайм-аут. 
Если в конкретной ситуации требуется завершить еще выполняющиеся задачи, то следовало бы явно обойти множество pending 
и  вызвать для каждой задачи cancel.
"""

if __name__ == '__main__':
    asyncio.run(main())
