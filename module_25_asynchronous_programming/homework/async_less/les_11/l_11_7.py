import asyncio
from asyncio import Semaphore
from aiohttp import ClientSession
from aiolimiter import AsyncLimiter


async def get_url(url: str,
                  session: ClientSession,
                  semaphore: Semaphore,
                  limiter: AsyncLimiter):
    print('Waiting to acquire semaphore...')
    async with semaphore:
        async with limiter:
            print('Acquired semaphore, requesting...')
            response = await session.get(url)
            print('Finished requesting')
            return response.status


async def main():
    # Создается семафор с максимальным количеством одновременных запросов равным 10.
    # Создается ограничитель скорости, позволяющий не более 10 запросов в секунду.
    semaphore = Semaphore(10)
    rate_limit = AsyncLimiter(10, 1)
    async with ClientSession() as session:
        tasks = [get_url('https://www.example.com', session, semaphore, rate_limit)
                 for _ in range(1000)]
        await asyncio.gather(*tasks)


asyncio.run(main())

"""
После каждого завершения запроса семафор освобождается, а зна- чит, задача, заблокированная в  ожидании семафора, 
может присту- пить к  работе. То есть в  каждый момент времени активно будет не более 10 запросов.
Это решает проблему слишком большого числа конкурентных за- просов, но теперь код демонстрирует пульсирующую нагрузку, 
т. е. за- просы могут отправляться пачками по 10, создавая пики трафика. Это может оказаться нежелательно, если пиков 
нагрузки на вызываемый API хотелось бы избежать. Если требуется ограничить всплески опре- деленным числом запросов в 
единицу времени, то следует воспользо- ваться каким-нибудь алгоритмом формирования трафика, например 
«дырявым ведром» или «корзиной маркеров».
"""