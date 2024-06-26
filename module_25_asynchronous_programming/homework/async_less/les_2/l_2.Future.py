# 2.5 Задачи, сопрограммы, будущие объекты и объекты, допускающие ожидание. Основы будущий объектов
from asyncio import Future, InvalidStateError

my_future = Future()

print('Completed?', my_future.done())

try:
    print(f'{my_future.result()=}')
except InvalidStateError as er:
    print('Исключение, потому что не было передано значение')
    print(er)

my_future.set_result(42)

print('Completed?', my_future.done())

print(f'{my_future.result()=}')
