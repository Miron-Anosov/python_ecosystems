# 2.5 Задачи, сопрограммы, будущие объекты и объекты, допускающие ожидание. Ожидание будущих объектов.
import asyncio
from asyncio import Future


def make_request() -> Future:
    my_future = Future()
    asyncio.create_task(set_future_volume(future=my_future))
    return my_future


async def set_future_volume(future) -> None:
    await asyncio.sleep(1)
    future.set_result(42)


async def main():
    future = make_request()
    print('Completed?', future.done())
    volume = await future
    print('Completed?', future.done())
    print(volume)

if __name__ == '__main__':
    asyncio.run(main())
