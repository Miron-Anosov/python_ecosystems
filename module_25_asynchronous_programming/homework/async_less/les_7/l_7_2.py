from threading import Thread
import socket


class ClientEchoThread(Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        try:
            while True:
                data = self.client.recv(2048)  # Получаем на вход данные
                if not data:  # Если данных больше нет, вызываем исключение
                    raise BrokenPipeError('Connection closed!')
                print(f'Received {data}, sending!')
                self.client.sendall(data)
        except OSError as e:
            print(f'Thread interrupted by {e} exception, shutting down!')

    def close(self):  # Уведомляется о закрытии соединения клиент и закрывается сокет.
        if self.is_alive():
            self.client.sendall(bytes('Shutting down!', encoding='utf-8'))
            self.client.shutdown(socket.SHUT_RDWR)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8080))
    server.listen()
    connection_threads = []
    try:
        while True:
            connection, addr = server.accept()  # Ожидаем новое подключение
            thread = ClientEchoThread(connection)  # Создается новый потом
            connection_threads.append(thread)  # Сохраняются в список все созданные потоки
            thread.start()  # Выполнение потока
    except KeyboardInterrupt:
        print('Shutting down!')
        [thread.close() for thread in connection_threads]