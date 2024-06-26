import asyncio
from module_25_asynchronous_programming.homework.async_less.util import delay, async_timed


async def positive_integers_async(until: int):
    for integer in range(1, until):
        await delay(integer)
        yield integer


@async_timed()
async def main():
    async_generator = positive_integers_async(3)
    print(type(async_generator))
    async for number in async_generator:
        print(f'Got number {number}')


asyncio.run(main())

"""
Как видим, это не обычный генератор, а объект типа `<class 'async_generator'>`. Асинхронный генератор отличается от 
обычного тем, что отдает не объекты Python, а генерирует сопрограммы, которые могут ждать получения результата с 
помощью `await`. Поэтому обычные циклы `for` и функция `next` с такими генераторами работать не будут. А вместо них 
предложена специальная синтаксическая конструкция `async for`. В данном примере мы использовали ее, чтобы обойти целые 
числа в сопрограмме `positive_integers_async`.

Этот код напечатает числа 1 и 2, но будет ждать 1 с перед возвратом первого числа и 2 с перед возвратом второго. 
Отметим, что генератор не выполняет порожденные сопрограммы конкурентно, а порождает и ждет их одну за другой.
"""
