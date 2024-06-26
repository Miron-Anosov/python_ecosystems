# Попытка создать состояние гонки.
import asyncio

counter: int = 0


async def increment():
    global counter
    await asyncio.sleep(0.01)
    counter = counter + 1


async def main():
    global counter
    for _ in range(1000):
        tasks = [asyncio.create_task(increment()) for _ in range(100)]
        await asyncio.gather(*tasks)
        print(f'Counter is {counter}')
        assert counter == 100
        counter = 0


asyncio.run(main())

"""
Означает ли это, что модель однопоточной конкурентности подарила нам способ раз и навсегда избавиться от гонок? 
К сожалению, нет. Хотя мы избежали гонки там, где одна неатомарная операция могла бы привести к ошибке, осталась 
проблема неправильного порядка выполнения нескольких операций. Чтобы посмотреть, как это бывает, сделаем операцию 
инкрементирования целого числа неатомарной, на взгляд asyncio.
"""