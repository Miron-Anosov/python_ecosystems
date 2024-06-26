import asyncio
from asyncio import Semaphore


async def acquire(semaphore: Semaphore):
    print('Waiting to acquire')
    async with semaphore:
        print('Acquired')
        await asyncio.sleep(5)
    print('Releasing')


async def release(semaphore: Semaphore):
    print('Releasing as a one off!')
    semaphore.release()
    print('Released as a one off!')


async def main():
    semaphore = Semaphore(2)

    print("Acquiring twice, releasing three times...")
    await asyncio.gather(acquire(semaphore),
                         acquire(semaphore),
                         release(semaphore))

    print("Acquiring three times...")
    await asyncio.gather(acquire(semaphore),
                         acquire(semaphore),
                         acquire(semaphore))


asyncio.run(main())


"""Листинг 11.8: Освобождений больше, чем захватов
Здесь мы создаем семафор с пределом 2. Затем дважды вызываем сопрограмму acquire и один раз release, т. е. 
всего семафор будет освобожден трижды. Первое обращение к gather завершается. Однако при втором обращении, 
когда мы захватываем семафор три раза, возникают проблемы – все три захвата происходят сразу! 
Мы непреднамеренно превысили предел семафора.
"""