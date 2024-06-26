import asyncio
from asyncio import Lock


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


async def user_disconnect(username: str, user_lock: Lock):
    print(f'{username} disconnected!')
    async with user_lock: #A
        print(f'Removing {username} from dictionary')
        socket = user_names_to_sockets.pop(username)
        socket.close()


async def message_all_users(user_lock: Lock):
    print('Creating message tasks')
    async with user_lock: #B
        messages = [socket.send(f'Hello {user}')
                    for user, socket
                    in user_names_to_sockets.items()]
        await asyncio.gather(*messages)


async def main():
    user_lock = Lock()
    await asyncio.gather(message_all_users(user_lock),
                         user_disconnect('Eric', user_lock))


asyncio.run(main())

"""
Сначала мы захватываем блокировку и создаем задачи для рассылки сообщений. Пока мы этим заняты, Эрик отключается, 
а код в сопрограмме `user_disconnect` пытается захватить блокировку. Поскольку `message_all_users` ещё удерживает её, 
придётся подождать освобождения, прежде чем мы сможем отключить пользователя. Это даёт возможность закончить рассылку 
до закрытия сокета и тем самым предотвратить ошибку.

Маловероятно, что вам часто понадобится использовать блокировки в коде на основе asyncio, потому что многие проблемы 
вообще не возникают в силу однопоточности модели. Но даже если состояния гонки имеют место, иногда удаётся переработать 
код так, чтобы состояние не модифицировалось в момент, когда сопрограмма приостановлена 
(например, использовать неизменяемые объекты). Если это невозможно, то блокировки хотя бы помогут гарантировать, что 
модификации производятся в желаемом синхронизированном порядке.
"""
