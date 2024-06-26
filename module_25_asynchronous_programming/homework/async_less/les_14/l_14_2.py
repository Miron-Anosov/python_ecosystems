# Листинг 14.2 Сервер с контекстными переменными

import asyncio
from asyncio import StreamReader, StreamWriter
from contextvars import ContextVar


class Server:
    user_address = ContextVar('user_address')  # Создать контекстную переменную с именем user_address

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def start_server(self):
        server = await asyncio.start_server(self._client_connected, self.host, self.port)
        await server.serve_forever()

    def _client_connected(self, reader: StreamReader, writer: StreamWriter):
        self.user_address.set(writer.get_extra_info('peername'))
        """В момент подключения пользователя сохранить его адрес в контекстной переменной"""
        asyncio.create_task(self.listen_for_messages(reader))

    async def listen_for_messages(self, reader: StreamReader):
        """Вывести сообщение пользователя и адрес отправителя, взятый из контекстной переменной"""
        while data := await reader.readline():
            print(f'Получено сообщение {data} от {self.user_address.get()}')


async def main():
    server = Server('127.0.0.1', 9000)
    await server.start_server()


asyncio.run(main())

"""
Здесь мы сначала создаем экземпляр класса `ContextVar`, в котором будем хранить информацию об адресе пользователя. 
Для этого нужно задать имя контекстной переменной, в данном случае мы назвали её `user_address`, в основном для отладки.
 Затем в функции обратного вызова `_client_connected` мы записываем в эту контекстную переменную адрес клиента. 
 Это позволит получить доступ к информации об адресе любой задаче, созданной родительской задачей; в данном случае 
 таковыми являются задачи прослушивания сообщений от клиентов.
В методе-сопрограмме `listen_for_messages` мы ожидаем сообщения от клиента и, получив его, печатаем вместе с адресом, 
хранящимся в контекстной переменной.
"""