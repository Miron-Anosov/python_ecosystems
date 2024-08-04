# Этот модуль получает сырые данные от api кофе и клиентов, валидирует и возвращает кортеж
# В случае, если сторонний сервис упал, будут возвращены константные данные для последующей их записи в БД.

import sys
import traceback

from aiohttp import ClientResponseError, ServerTimeoutError

from .generator_data import generate_run
from ..validators.coffee_validate import CoffeeValidatorInput
from ..validators.user_validate import UserValidatorInput
from .data_if_api_fail import users, coffee

USER_INDEX = 0
COFFEE_INDEX = 1


def make_data_for_db() -> tuple[list[dict], list[dict]]:
    """
    Функция обрабатывает данные, полученные из API, и преобразует их в валидные модели Pydantic.

    Returns:
        tuple:
        - list[CoffeeValidatorInput]
        - list[UserValidatorInput]
    """
    coffee_data_from_api: list[dict] = []
    user_data_from_api: list[dict] = []

    try:
        data_from_api = generate_run()
    except (ClientResponseError, ServerTimeoutError) as e:
        stack_trace = ''.join(traceback.format_stack())
        print(f'НЕВОЗМОЖНО ПОЛУЧИТЬ ДАННЫЕ ОТ СТОРОННЕГО СЕРВИСА:'
              f' https://random-data-api.com.\n {stack_trace}\n{e}', file=sys.stderr)
        return coffee, users

    for coffee_for_validate, user_address in zip(data_from_api[COFFEE_INDEX], data_from_api[USER_INDEX]):
        coffee_for_validate["notes"] = coffee_for_validate["notes"].split(', ')
        new_coffee = CoffeeValidatorInput(**coffee_for_validate).model_dump()
        coffee_data_from_api.append(new_coffee)

        user_for_validate = dict()
        user_for_validate["name"] = f"user_{len(user_data_from_api)}"
        user_for_validate['address'] = user_address
        new_user = UserValidatorInput(**user_for_validate).model_dump()
        user_data_from_api.append(new_user)

    return coffee_data_from_api, user_data_from_api
