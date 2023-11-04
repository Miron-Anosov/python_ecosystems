"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

import traceback
from typing import Collection, Type, Literal, List
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection) -> None:
        self.errors: tuple = tuple(set(errors))

    def __enter__(self) -> None:
        ...

    def __exit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None,
                 exc_tb: TracebackType | None) -> Literal[True] | None:
        if exc_type:
            if issubclass(exc_type, self.errors):
                return True
            else:
                raise exc_val


if __name__ == '__main__':
    err_types = {ZeroDivisionError}
    with BlockErrors(err_types):
        a = 1 / 0
    print('Выполнено без ошибок')
