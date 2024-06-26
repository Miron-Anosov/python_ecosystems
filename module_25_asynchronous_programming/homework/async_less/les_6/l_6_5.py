import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List


def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter = counter + 1
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [1, 3, 5, 22, 100000000]
        calls: List[partial[int]] = [partial(count, num) for num in nums]
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))

        # results = await asyncio.gather(*call_coros)
        # for result in results:
        #     print(result)

        for finished_task in asyncio.as_completed(call_coros):
            result = await finished_task
            print(f'Finished counting with {result} ')
            print(result)


if __name__ == "__main__":
    asyncio.run(main())

"""
Сначала мы, как и раньше, создаем исполнитель пула процессов. Затем получаем цикл событий asyncio, поскольку 
run_in_executor – метод класса AbstractEventLoop. Затем с помощью частичного применения функции вызываем count с каждым 
числом из списка nums в качестве аргумента, поскольку прямой вызов с аргументом невозможен. Сформированные вызовы 
функции count можно передать исполнителю. Мы обходим эти вызовы в цикле, вызывая loop.run_in_executor для каждого и 
сохраняя полученные в ответ объекты, допускающие ожидание, в списке call_coros. Затем передаем этот список функции 
asyncio.gather и ждем завершения всех вызовов. При желании можно было бы также использовать функцию asyncio.as_completed 
для получения результатов дочерних процессов по мере их готовности. Тем самым мы решили бы проблему рассмотренного выше 
метода пула процессов map в случае, если бы какая-то задача занимала много времени.
"""
