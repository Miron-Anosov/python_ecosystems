#  Отмена медленного запроса

import aiohttp
import asyncio

from module_25_asynchronous_programming.homework.async_less.util import fetch_status


async def main():
    async with aiohttp.ClientSession() as client:
        good_request = fetch_status(client=client, url="https://example.com")
        request_long = fetch_status(client=client, url="https://example.com", delay=2)

        done, pending = await asyncio.wait([good_request, request_long], timeout=1)

        for pend in pending:
            if pend is request_long:
                print('Длительный запрос не был выполнен')
                pend.cancel()


"""
Заметим, что, как и раньше, задачи в множестве pending не сняты и продолжают работать, несмотря на тайм-аут. 
Если в конкретной ситуации требуется завершить еще выполняющиеся задачи, то следовало бы явно обойти множество
pending и  вызвать для каждой задачи cancel. 

# В обновленной версии пробрасывается библиотеки исключение RuntimeWarning: coroutine 'fetch_status' was never awaited
"""

if __name__ == '__main__':
    asyncio.run(main())
