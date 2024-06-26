# Попытка отправить сообщение клиенту в состоянии гонки.

import asyncio


class MockSocket:
    def __init__(self):
        self.socket_closed = False

    async def send(self, msg: str):
        if self.socket_closed:
            raise Exception('Socket is closed!')
        print(f'Sending: {msg}')
        await asyncio.sleep(1)
        print(f'Sent: {msg}')

    def close(self):
        self.socket_closed = True


user_names_to_sockets = {'John': MockSocket(),
                         'Terry': MockSocket(),
                         'Graham': MockSocket(),
                         'Eric': MockSocket()}


async def user_disconnect(username: str):
    print(f'{username} disconnected!')
    socket = user_names_to_sockets.pop(username)
    socket.close()


async def message_all_users():
    print('Creating message tasks')
    messages = [socket.send(f'Hello {user}')
                for user, socket
                in user_names_to_sockets.items()]
    await asyncio.gather(*messages)


async def main():
    await asyncio.gather(message_all_users(), user_disconnect('Eric'))


asyncio.run(main())

"""
Здесь мы сначала создаем задачи отправки сообщений, а затем выполняем предложение `await`, приостанавливающее 
сопрограмму `message_all_users`. Это даёт шанс выполниться сопрограмме `user_disconnect('Eric')`, которая закрывает 
сокет Эрика и удаляет его из словаря `user_names_to_sockets`. Затем сопрограмма `message_all_users` возобновляется, 
и мы начинаем рассылать сообщения. Так как сокет Эрика уже закрыт, мы получаем исключение, а Эрик не получит 
адресованного ему сообщения. Отметим, что мы также модифицировали словарь `user_names_to_sockets`. Если бы мы 
использовали его, рассчитывая, что Эрик всё ещё там, то могли бы нарваться на исключение или ещё какую-нибудь ошибку.
"""