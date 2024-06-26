# Листинг 3.10 Корректная остановка

import asyncio
import logging
import socket
from asyncio import AbstractEventLoop


async def echo(connection: socket.socket, loop: AbstractEventLoop):
    try:
        while data := await loop.sock_recv(connection, 1024):
            if b'error' in data:
                raise Exception(data)
            await loop.sock_sendall(connection, data)
    except Exception as err:
        logging.exception(err)
    finally:
        connection.close()


async def listening_new_connection(server_socker: socket.socket, loop: AbstractEventLoop):
    while True:
        conn, address = await loop.sock_accept(server_socker)
        conn.setblocking(False)
        print('Подключен:', address)
        asyncio.create_task(echo(connection=conn, loop=loop))


async def main():
    server_address = '127.0.0.1', 8080
    server_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listening_new_connection(server_socket, asyncio.get_event_loop())


if __name__ == '__main__':
    asyncio.run(main())
