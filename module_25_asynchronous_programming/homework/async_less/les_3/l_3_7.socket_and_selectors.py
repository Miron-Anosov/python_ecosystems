# Листинг 3.7 Использование селектора для построения неблокирующего сервера

import socket
import selectors
from selectors import SelectorKey
from typing import List, Tuple

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8080)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)  # регистрируется сокет сервера

while True:
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

    if not len(events):
        print('Сообщений нет.')

    for event, _ in events:
        event_socket = event.fileobj  # Получаем объект сокета, вызвавший событие

        if event_socket == server_socket:
            # Если событие инициировано серверным сокетом, это значит, что поступило новое подключение
            connection, address = server_socket.accept()  # Принимаем новое соединение
            connection.setblocking(False)  # Устанавливаем неблокирующий режим для нового клиентского сокета
            print('Подключение: ', address)
            selector.register(connection,
                              selectors.EVENT_READ)  # Регистрируем новый клиентский сокет для событий чтения

        else:
            # Если событие инициировано клиентским сокетом, это значит, что поступили данные от клиента
            data = event_socket.recv(1024)  # Читаем данные из клиентского сокета
            if data:
                print('Полученные данные:', data)
                event_socket.send(data)  # Отправляем данные обратно клиенту (эхо-сервер)
            else:
                # Если данных нет, это означает, что клиент закрыл соединение
                print('Соединение закрыто')
                selector.unregister(event_socket)  # Удаляем сокет из селектора
                event_socket.close()  # Закрываем сокет

