import time
from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter = counter + 1
    end = time.time()
    print(f'Finished counting to {count_to} in {end - start}')
    return counter


if __name__ == "__main__":
    with ProcessPoolExecutor() as process_pool:
        numbers = [1, 3, 5, 22, 100000000]
        for result in process_pool.map(count, numbers):
            print(f"{result=}")


"""
Хотя кажется, что программа работает так же, как asyncio.as_completed, на самом деле порядок итераций детерминирован и 
определяется тем, в каком порядке следуют числа в списке numbers. Это значит, что если бы первым числом было 100000000, 
то пришлось бы ждать завершения соответствующего вызова, и только потом появилась бы возможность напечатать другие 
результаты, хотя они и были вычислены раньше. То есть эта техника не такая отзывчивая, как функция asyncio.as_completed.
"""
