import asyncio
from enum import Enum


class ConnectionState(Enum):
    WAIT_INIT = 0
    INITIALIZING = 1
    INITIALIZED = 2


class Connection:

    def __init__(self):
        self._state = ConnectionState.WAIT_INIT
        self._condition = asyncio.Condition()

    async def initialize(self):
        await self._change_state(ConnectionState.INITIALIZING)
        print('initialize: Initializing connection...')
        await asyncio.sleep(3)  # simulate connection startup time
        print('initialize: Finished initializing connection')
        await self._change_state(ConnectionState.INITIALIZED)

    async def execute(self, query: str):
        async with self._condition:
            print('execute: Waiting for connection to initialize')
            await self._condition.wait_for(self._is_initialized)
            print(f'execute: Running {query}!!!')
            await asyncio.sleep(3)  # simulate a long query

    async def _change_state(self, state: ConnectionState):
        async with self._condition:
            print(f'change_state: State changing from {self._state} to {state}')
            self._state = state
            self._condition.notify_all()

    def _is_initialized(self):
        if self._state is not ConnectionState.INITIALIZED:
            print(f'_is_initialized: Connection not finished initializing, state is {self._state}')
            return False
        print(f'_is_initialized: Connection is initialized!')
        return True


async def main():
    connection = Connection()
    query_one = asyncio.create_task(connection.execute('select * from table'))
    query_two = asyncio.create_task(connection.execute('select * from other_table'))
    asyncio.create_task(connection.initialize())
    await query_one
    await query_two


asyncio.run(main())

"""
Здесь мы написали класс подключения, содержащий объект условия и хранящий внутреннее состояние, которое мы 
инициализировали значением WAIT_INIT, показывающим, что мы ждем завершения инициализации. В классе Connection 
имеется несколько методов.

Метод initialize моделирует создание подключения к базе данных. Он вызывает метод _change_state, который сначала 
устанавливает состояние в INITIALIZING, а затем, когда подключение инициализировано, изменяет его на INITIALIZED. 
В методе _change_state мы устанавливаем внутреннее состояние, а затем вызываем метод условия notify_all, который 
пробуждает все задачи, ожидающие условия.

В методе execute мы захватываем объект условия в блоке async with, после чего вызываем wait_for с предикатом, 
проверяющим, равно ли состояние INITIALIZED. Эта проверка блокирует выполнение, пока подключение к базе данных не будет
полностью инициализировано, что предотвращает случайное выполнение запроса в момент, когда подключения еще не существует.

Затем в сопрограмме main мы создаем экземпляр класса подключения, две задачи для выполнения запросов и 
еще одну для инициализации подключения.
"""