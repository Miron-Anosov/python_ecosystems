#  Обработка исключений при помощи wait по мере выполнения задач

import asyncio
import logging
import aiohttp

from module_25_asynchronous_programming.homework.async_less.util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as client:
        good_request = fetch_status(client=client, url="https://example.com")
        good_request_2 = fetch_status(client=client, url="https://example.com")
        good_request_3 = fetch_status(client=client, url="https://example.com")
        bad_request = fetch_status(client=client, url="ssh://example.com")

        pending = [asyncio.create_task(good_request),
                   asyncio.create_task(bad_request),
                   asyncio.create_task(good_request_2),
                   asyncio.create_task(good_request_3),
                   ]

        while pending:
            # asyncio.wait(return_when=ALL_COMPLETED) default
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            print(f'Число завершенных задач: {len(done)}')
            print(f'Число не завершенных задач: {len(pending)}')

            for done_task in done:
                # result = await done_task возбудит исключение
                if done_task.exception() is None:
                    print(done_task.result())
                else:
                    # Обрабатываем ошибку
                    logging.error('Ошибка запроса', exc_info=done_task.exception())


""" 
asyncio.wait(FIRST_EXCEPTION)
Если ни один допускающий ожидание объект не возбудил исключения
Если ни в одной задаче не было исключений, то этот режим эквивалентен ALL_COMPLETED. 
Мы дождемся завершения всех задач, после чего множество done будет содержать все задачи,
а  множество pending останется пустым.

Если в одной или нескольких задачах возникло исключение
Если хотя бы в одной задаче возникло исключение, то wait немедленно возвращается. 
Множество done будет содержать как задачи, завершившиеся успешно, так и те, в которых имело место исключение. 
Гарантируется, что done будет содержать как минимум одну задачу – завершившуюся ошибкой, но может содержать и  какие-то 
успешно завершившиеся задачи. Множество pending может быть пустым, а  может содержать задачи, 
которые продолжают выполняться. Мы можем использовать его для управления выполняемыми задачами по своему усмотрению.
"""

if __name__ == '__main__':
    asyncio.run(main())
