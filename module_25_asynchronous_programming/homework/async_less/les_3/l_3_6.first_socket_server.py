# Листинг 3.6 Перехват и игнорирование ошибок блокирующего ввода-вывода
# Из-за перехвата исключений в бесконечном цикле потребление процессора быстро доходит до 100% и на этом уровне остается

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('127.0.0.1', 8080)
    server_socket.bind(address)
    server_socket.listen()
    connections = list()
    server_socket.setblocking(False)
    # server_socket.settimeout(1.0)

    try:
        print('Сервер запушен ...')
        while True:
            try:
                connect, client_address = server_socket.accept()
                print(f'Получен запрос на подключение от {client_address}!')
                connect.setblocking(False)
                connections.append(connect)
            except BlockingIOError:
                pass

            for conn in connections[:]:
                try:
                    buffer = b''
                    while True:

                        data = conn.recv(1024)
                        if not data:
                            print('Соединение закрыто!')
                            connections.remove(conn)
                            conn.close()
                            break

                        print(f"Получены данные: {data}")

                        buffer += data
                        if buffer.endswith(b'\r\n'):
                            print(f"Эхо данные: {buffer}")

                            conn.sendall(buffer)

                except BlockingIOError:
                    pass

    except KeyboardInterrupt:
        server_socket.close()
        print('EXIT')
