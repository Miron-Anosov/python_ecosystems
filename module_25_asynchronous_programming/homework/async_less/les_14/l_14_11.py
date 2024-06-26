# Листинг 14.8 Реализация класса CustomFuture
from l_14_8 import CustomFuture


class CustomTask(CustomFuture):

    def __init__(self, coro, loop):
        super(CustomTask, self).__init__()
        self._coro = coro  # Сопрограмма, которую будет выполнять задача.
        self._loop = loop  # цикл событий, в котором будет выполняться задача
        self._current_result = None
        self._task_state = None
        loop.register_task(self)  # Зарегистрировать задачу в цикле событий.

    def step(self):  # Выполнить один шаг сопрограммы
        try:
            if self._task_state is None:  # Если это первый шаг, запускает сопрограмму.
                self._task_state = self._coro.send(None)
            if isinstance(self._task_state, CustomFuture):
                # Если сопрограмма отдает будущий объект, вызвать add_done_callback
                self._task_state.add_done_callback(self._future_done)
        except StopIteration as si:
            self.set_result(si.value)

    def _future_done(self, result):  # Когда будущий объект будет готов, отправить результат сопрограмме
        self._current_result = result
        try:
            self._task_state = self._coro.send(self._current_result)
        except StopIteration as si:
            self.set_result(si.value)


"""
Задача представляет собой комбинацию будущего объекта и сопрограммы. Будущий объект задачи завершается, когда 
завершается обернутая им сопрограмма. Обернуть сопрограмму будущим объектом можно, унаследовав классу CustomFuture и 
написав конструктор, который принимает сопрограмму, но необходим еще способ выполнить сопрограмму. Это можно сделать, 
написав метод step, который будет вызывать метод сопрограммы send и запоминать результат, т. е. выполнять один шаг 
сопрограммы при каждом вызове.
При реализации этого метода следует иметь в виду, что send может возвращать также другие будущие объекты. Чтобы 
обработать эту ситуацию, мы должны использовать метод add_done_callback любого будущего объекта, возвращаемого send. 
Мы зарегистрируем обратный вызов, который будет вызывать метод send сопрограммы задачи по готовности будущего объекта и 
передавать ему результирующее значение
Здесь  мы  создаем  подкласс CustomFuture,  конструктор  которого принимает сопрограмму и цикл событий и регистрирует
задачу в цикле, вызывая метод loop.register_task. Затем в методе step мы вызываем метод send сопрограммы и если 
сопрограмма отдает объект типа CustomFuture, то добавляем обратный вызов done. В данном случае done принимает результат 
будущего объекта и отправляет его обернутой сопрограмме, продвигая ее вперед в момент, 
когда будущий объект оказывается готов.
"""