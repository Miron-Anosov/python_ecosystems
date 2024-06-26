#  Листинг 3.10 Корректная остановка

import asyncio
import logging
import signal
import socket
from asyncio import AbstractEventLoop
from typing import List

# Список для хранения задач echo
echo_tasks = list()


# Исключение для корректного завершения
class GracefulExit(SystemExit):
    pass


# Функция для завершения работы при получении сигнала
def shutdown():
    raise GracefulExit()


# Асинхронная функция echo для обработки данных от клиента
async def echo(connection: socket.socket, loop_: AbstractEventLoop):
    try:
        while data := await loop_.sock_recv(connection, 1024):  # Чтение данных асинхронно
            if b'error' in data:
                raise Exception(data)  # Генерация исключения при наличии 'error' в данных
            await loop_.sock_sendall(connection, data)  # Отправка данных обратно клиенту
    except Exception as err:
        logging.exception(err)
    finally:
        connection.close()  # Закрытие соединения


# Асинхронная функция для корректного завершения задач
async def close_echo_task(echo_tks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tks]  # Ограничение времени ожидания 2 секундами
    for task in waiters:
        try:
            await task  # Ожидание завершения задачи
        except asyncio.TimeoutError:
            print('Ожидаем истечения тайм-аута')


# Асинхронная функция для прослушивания новых подключений
async def connection_listener(server_socket: socket.socket, loop__: AbstractEventLoop):
    while True:
        connection, address = await loop__.sock_accept(server_socket)  # Ожидание нового подключения
        connection.setblocking(False)
        print('Message from:', address)
        echo_task = asyncio.create_task(echo(connection=connection, loop_=loop__))  # Создание задачи для echo
        echo_tasks.append(echo_task)  # Добавление задачи в список


# Основная функция
async def main(loop: asyncio.AbstractEventLoop):
    address = '127.0.0.1', 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    server_socket.setblocking(False)
    server_socket.listen()

    # Установка обработчиков сигналов для корректного завершения
    for sig_name in 'SIGINT', 'SIGTERM':
        loop.add_signal_handler(getattr(signal, sig_name), shutdown)

    await connection_listener(server_socket, loop)  # Запуск прослушивания подключений


if __name__ == '__main__':
    event_loop = asyncio.new_event_loop()  # Создание нового цикла событий
    try:
        event_loop.run_until_complete(main(loop=event_loop))  # Запуск основной функции
    except GracefulExit:
        event_loop.run_until_complete(close_echo_task(echo_tasks))  # Корректное завершение задач
    finally:
        event_loop.close()  # Закрытие цикла событий
"""
Если остановить приложение нажатием CTRL+C или командой kill в момент, когда подключен хотя бы один клиент, то будет
выполнена логика остановки. 
Мы увидим, что приложение ждет 2 с, давая зада- чам echo возможность завершиться, а затем останавливается.
Есть две причины, по которым эта логика несовершенна. 
Во-пер- вых, ожидая завершения задач echo, мы не останавливаем прослуши- ватель подключений. 
Это значит, что, пока мы ждем, может поступить новый запрос на подключение,
для которого мы не сможем добавить двухсекундный тайм-аут. Во-вторых, мы ждем завершения всех задач echo, 
но перехватываем только исключения TimeoutException. Следо- вательно, если задача возбудит какое-то другое исключение,
мы его запомним, а все последующие задачи, возбуждающие исключение, будут проигнорированы. 
"""
