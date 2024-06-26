
import asyncio
from asyncio import BoundedSemaphore


async def main():
    semaphore = BoundedSemaphore(1)

    await semaphore.acquire()
    semaphore.release()
    semaphore.release()


asyncio.run(main())

"""
Для таких ситуаций asyncio предлагает класс BoundedSemaphore. Ведет он себя так же, как обычный, с одним отличием: при
попытке вызвать метод release таким образом, что это изменит допустимый предел захватов, возбуждается исключение
ValueError: BoundedSemaphore released too many times. В листинге ниже приведен очень простой пример. Здесь второй вызов
release возбудит исключение ValueError, означающее, что мы освободили семафор слишком много раз. Аналогичный результат
будет иметь место, если в листинге 11.8 использовать BoundedSemaphore вместо Semaphore. Если вы вызываете acquire и
release вручную, так что возникает опасность динамически превысить предел семафора, то лучше работать
с BoundedSemaphore, потому что возникшее исключение предупредит об ошибке.
"""