# Листинг 14.13 Реализация сервера

import socket

from l_14_12 import EventLoop
from l_14_11 import CustomTask


async def read_from_client(conn, loop: EventLoop):
    """Читать и протоколировать данные от клиента"""
    print(f'Чтение данных от клиента {conn}')
    try:
        while data := await loop.sock_recv(conn):  # отдаем управление
            print(f'Получены данные {data} от клиента!')
    finally:
        loop.sock_close(conn)


async def listen_for_connections(sock, loop: EventLoop):
    """Прослушать запросы на подключения и создать задачу для чтения данных от подключившегося клиента"""
    while True:
        print('Ожидание подключения...')
        conn, addr = await loop.sock_accept(sock)
        CustomTask(coro=read_from_client(conn, loop), loop=loop)
        print(f'Новое подключение к сокету {sock}!')


async def main(loop: EventLoop):
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('localhost', 8000))
    server_socket.listen()
    server_socket.setblocking(False)

    await listen_for_connections(server_socket, loop)


event_loop = EventLoop()  # Создать экземпляр цикла событий и выполнять в нем сопрограмму main
event_loop.run(main(event_loop))

"""
Здесь мы сначала определяем сопрограмму, которая в цикле читает и печатает данные от клиента. Также определяем 
сопрограмму, которая в бесконечном цикле прослушивает запросы на подключение к серверному сокету и создает экземпляр 
CustomTask, чтобы конкурентно читать данные от подключившегося клиента. В сопрограмме main мы создаем серверный сокет 
и вызываем сопрограмму listen_for_connections. Затем создаем экземпляр цикла событий и передаем его методу run 
сопрограммы main.
Запустив эту программу, мы сможем одновременно подключить к ней несколько клиентов telnet и отправлять сообщения серверу
Мы видим, что первый клиент подключается, в результате чего селектор  возобновляет  работу  сопрограммы 
listen_for_connections, приостановленную на обращении к loop.sock_accept. При этом в селекторе регистрируется клиентское
подключение, т.е. мы создаем задачу для сопрограммы read_from_client. Первый клиент отправляет сообщение
«test from client one!», что заставляет селектор выполнить все зарегистрированные обратные вызовы. В данном случае мы 
продвигаем вперед  задачу read_from_client, которая выводит полученное от клиента сообщение на консоль. 
Затем подключается второй клиент, и весь процесс повторяется.
"""