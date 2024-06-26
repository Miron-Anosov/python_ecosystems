# Листинг 3.8 Построение асинхронного эхо-сервера

import asyncio
import socket
from asyncio import AbstractEventLoop


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    # в бесконечном цикле ожидаем данные от клиента.
    while data := await loop.sock_recv(connection, 1024):
        await loop.sock_sendall(connection, data)  # получив данные отправляем их обратно клиенту


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print('Подключен:', address)
        asyncio.create_task(echo(connection, loop))
        #  После получения запроса на подключение создаем задачу echo, ожидающую данные от клиента


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = '127.0.0.1', 8080
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listen_for_connection(server_socket, asyncio.get_event_loop())

if __name__ == '__main__':
    asyncio.run(main())
