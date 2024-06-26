# Асинхронные контекстные менеджеры

import asyncio
import socket
from types import TracebackType
from typing import Type, Optional


class ConnectedSocket:

    def __init__(self, server_socket: socket.socket):
        self._server_socket = server_socket
        self._connection: Optional[socket.socket] = None

    async def __aenter__(self):
        print('Ожидание подключения...')
        loop = asyncio.get_event_loop()
        connection, address = await loop.sock_accept(self._server_socket)
        connection.setblocking(False)
        print('Подключен:', address)
        self._connection = connection
        return self._connection

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException],
                        exc_tb: Optional[TracebackType]):
        print('Выход из контекстного менеджера.')
        self._connection.close()
        print('Соединение закрыто')


async def main():
    loop = asyncio.get_event_loop()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = '127.0.0.1', 8080
    server_socket.bind(address)
    server_socket.setblocking(False)
    server_socket.listen()

    async with ConnectedSocket(server_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        print(data)

if __name__ == '__main__':
    asyncio.run(main())

