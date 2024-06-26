import asyncio
from asyncio import Semaphore


async def operation(semaphore: Semaphore):
    print('Waiting to acquire semaphore...')
    async with semaphore:
        print('Semaphore acquired!')
        await asyncio.sleep(2)
    print('Semaphore released!')


async def main():
    semaphore = Semaphore(2)
    await asyncio.gather(*[operation(semaphore) for _ in range(4)])

asyncio.run(main())

"""
В сопрограмме `main` мы создаем семафор с пределом 2. Это означает, что мы сможем захватить его дважды, после чего 
дальнейшие попытки начнут блокироваться. Затем мы четыре раза конкурентно вызываем сопрограмму `operation` – она 
захватывает семафор в блоке `async with` и с помощью `sleep` имитирует блокирующую операцию.
"""
