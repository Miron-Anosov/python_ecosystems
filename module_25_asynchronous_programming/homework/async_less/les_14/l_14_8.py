from typing import Any


class CustomFuture:
    """
    Базовый класс для создания объектов, которые работают с future
    """

    def __init__(self):
        # Для объекта future мы не можем получить результат сразу, потому при инициализации результата нет.
        self._result = None
        self._is_finished = False
        self._done_callback = None

    def result(self) -> Any:
        """Возвращает результат."""
        return self._result

    def is_finished(self) -> bool:
        """Проверяет, завершён ли объект future."""
        return self._is_finished

    def set_result(self, result) -> None:
        """Устанавливает результат."""
        self._result = result
        self._is_finished = True  # Изменяем булево значение для того что объект future был завершён.
        if self._done_callback:  # Если есть обратный вызов, то вызываем его.
            self._done_callback(result)

    def add_done_callback(self, fn) -> None:
        """Добавляет обратный вызов."""
        self._done_callback = fn

    def __await__(self) -> Any:
        """Если итератор завершён, то мы возвращаем `self._result`."""
        if not self._is_finished:
            yield self
        return self.result()
        # Если результат уже установлен, то мы возвращаем результат и будет вызвано исключение StopIteration.


"""
Здесь определён класс `CustomFuture` с методом `__await__`, а также методами для установки результата, получения 
результата и добавления обратного вызова. Метод `__await__` проверяет, получено ли значение будущего объекта. 
Если да, то мы просто возвращаем результат, и итератор завершается. Если нет, то мы возвращаем `self`, то есть итератор 
будет возвращать себя до тех пор, пока значение не будет установлено. В терминах генераторов это означает, 
что `__await__` может вызываться бесконечно, пока кто-то не установит значение.
"""
