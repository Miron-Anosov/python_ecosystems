"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional, Callable
from flask_wtf import FlaskForm
from wtforms import Field, ValidationError


def number_length(min_value: int = 1, max_value: int = 999_999_99_99,
                  message: Optional[str] = None) -> Callable:
    """Функция выполняет роль валидатора которая проверяет числовые значения в рамках заданного диапазона."""
    if message:
        error = ValidationError(message)
    else:
        error = ValidationError(f'The phone must be number and between {min_value} and {max_value} characters long.')

    def _number_length(_: FlaskForm, field: Field):
        index = field.data
        try:
            if min_value > index or index > max_value:
                raise error
        except (AttributeError, TypeError):
            raise error

    return _number_length


class NumberLength:
    """Базовый класс представляющий собой валидацию числовых значений.
     Определяющий минимальную и максимальную длину числовых символов.
     """

    def __init__(self, min_len: int, max_len: int, message: Optional[str] = None):
        self.min_len = min_len
        self.max_len = max_len
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        try:
            data = field.data
            data = str(data)
            if not data.isdigit():
                raise ValidationError
            else:
                if self.min_len > len(data) or len(data) > self.max_len:
                    raise ValidationError
        except (ValidationError, AttributeError):
            if self.message:
                raise ValidationError(self.message)
            raise ValidationError(f'The index must be between {self.min_len} and {self.max_len}')
