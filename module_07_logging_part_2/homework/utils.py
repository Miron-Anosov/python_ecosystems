import logging

from typing import Union, Callable
from operator import sub, mul, truediv, add

logger = logging.getLogger('app.utils')

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """

    logger.info('Start string_to_operator, ---test ascii True---')
    logger.info(f' Value is validate: {value}')
    logger.info('Value check as str')
    if not isinstance(value, str):
        logger.error(f'Wrong operator type, type not must be {type(value)}, {value=}')
        raise ValueError("Wrong operator type, it's not str")
    logger.debug('Value is string')

    if value not in OPERATORS:
        logger.error(f'Wrong operator type, {value}, arithmetic function must be: ( + - * / )')
        raise ValueError("Wrong operator value, it's must be basic arithmetic function")

    logger.debug('Value is in OPERATORS')
    logger.info(f'Value is returns : {value}')
    logger.info('Сlose string_to_operator, ---test ascii False---')
    return OPERATORS[value]
