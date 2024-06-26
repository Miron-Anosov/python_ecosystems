# Листинг 14.12 Реализация цикла событий

import functools
import selectors

from l_14_8 import CustomFuture


class EventLoop:

    def __init__(self):
        # селектор, который будет использоваться для определения, какие события будут происходить
        self.selector = selectors.DefaultSelector()
        self._tasks_to_run = []  # список задач, которые нужно запустить
        self.current_result = None

    def _register_socket_to_read(self, sock, callback):
        """Зарегистрировать в селекторе сокет для событий чтения.
        Создать экземпляр Custom-Future, результат которого установит обратный вызов,
        и зарегистрировать этот обратный вызов в селекторе, чтобы он вызывался по событиям чтения.
        """
        future = CustomFuture()
        try:
            self.selector.get_key(sock)  # запрашивает событие.
        except KeyError:  # если событие не было найдено
            sock.setblocking(False)  # не блокирует сокет
            self.selector.register(sock, selectors.EVENT_READ,
                                   functools.partial(callback, future))  # Регистрирует событие
        else:
            # Изменяет отслеживаемые события или прикрепленные данные зарегистрированного сокета.
            self.selector.modify(sock, selectors.EVENT_READ, functools.partial(callback, future))
        return future

    def _set_current_result(self, result):
        self.current_result = result

    async def sock_recv(self, sock):
        """Зарегистрировать сокет для получения данных от клиента"""
        print('Регистрируется сокет для прослушивания данных...')
        return await self._register_socket_to_read(sock, self.recieved_data)

    async def sock_accept(self, sock):
        """ Зарегистрировать сокет для приема запросов на подключение от клиентов"""
        print('Регистрируется сокет для приема подключений...')
        return await self._register_socket_to_read(sock, self.accept_connection)

    def sock_close(self, sock):
        """Прекратить отслеживание сокета и его закрытие"""
        self.selector.unregister(sock)
        sock.close()

    def register_task(self, task):
        """Регистрирует задачу в цикле событий"""
        self._tasks_to_run.append(task)

    def recieved_data(self, future, sock):
        """Обработка полученных данных"""
        data = sock.recv(1024)
        future.set_result(data)

    def accept_connection(self, future, sock):
        """Обработка подключения клиента"""
        result = sock.accept()
        future.set_result(result)  # сопрограмма принимает результат сокета

    def run(self, coro):
        """Выполнять сопрограмму пока не завершится. На каждой итерации выполнять готовые к работе задачи"""
        self.current_result = coro.send(None)

        while True:
            try:
                if isinstance(self.current_result, CustomFuture):
                    # Если main возвращает будущий объект, то мы добавляем обратный вызов done,
                    # чтобы запомнить результат этого объекта, когда он будет готов
                    self.current_result.add_done_callback(self._set_current_result)
                    if self.current_result.result() is not None:  # если сопрограмма не завершилась
                        self.current_result = coro.send(self.current_result.result())
                else:
                    self.current_result = coro.send(self.current_result)
            except StopIteration as si:
                # Если где-то в сопрограмме main возбуждается исключение StopIteration, значит, приложение
                # завершилось и мы можем выйти, вернув значение, полученное в составе исключения.
                print('value =', si.value)
                return si.value

            # Затем вызывается метод step всех зарегистрированных задач и
            # проверяется, были ли события на сокетах селектора.
            for task in self._tasks_to_run:
                task.step()

            self._tasks_to_run = [task for task in self._tasks_to_run if not task.is_finished()]

            events = self.selector.select()
            print('В селекторе есть событие, обрабатывается...')
            for key, mask in events:
                callback = key.data
                callback(key.fileobj)


"""
Сначала определяется вспомогательный метод _register_socket_ to_read. Он принимает сокет и обратный вызов и регистрирует
их в селекторе, если сокет еще не зарегистрирован. Если же сокет зарегистрирован, то мы заменяем обратный вызов. 
Первым аргументом обратного вызова должен быть будущий объект, и в этом методе мы создаем его и привязываем к 
обратному вызову. Этот привязанный будущий объект возвращается, так что теперь вызывающая сторона может ожидать его с
помощью await, приостанавливая выполнение до готовности будущего объекта.
Затем следуют методы сопрограммы для получения данных из сокета и приема запросов на подключение: sock_recv и 
sock_accept. Они  вызывают  написанный  ранее  метод _register_socket_to_read и передают ему обратные вызовы для 
обработки данных и новых подключений (эти вызовы просто записывают полученные данные в будущий объект).
И наконец, метод run. Он принимает главную сопрограмму (точку входа) и вызывает ее метод send, продвигая к первой точке
приостановки, после чего сохраняет результат send. Затем мы входим в бесконечный цикл, где первым делом проверяем, 
является ли результат главной сопрограммы объектом типа CustomFuture; если да, то мы регистрируем обратный вызов для 
сохранения результата, который затем при необходимости можно будет отправить назад главной сопрограмме. В противном 
случае мы просто отправляем результат сопрограмме. Разобравшись с главной сопрограммой, выполняем все зарегистрированные
в цикле событий задачи, вызывая их метод step. После того как задачи получили возможность отработать, мы удаляем 
завершившиеся из списка задач.
Наконец, мы вызываем метод selector.select, который блокирует выполнение, пока на каком-то из зарегистрированных сокетов
не произойдет событие. Затем в цикле перебираем все возникшие события и для каждого вызываем функцию обратного вызова, 
зарегистрированную для  соответствующего  сокета  в методе _register_socket_to_read. В нашей реализации любое событие 
сокета приводит к очередной итерации цикла событий. 
"""