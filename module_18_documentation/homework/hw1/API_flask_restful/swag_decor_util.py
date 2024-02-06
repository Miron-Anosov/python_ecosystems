import json
from typing import Callable
from functools import wraps


def swagger_doc_from_json_to_pydict(call: Callable) -> Callable:
    @wraps(call)
    def wrapper(type_obj: str) -> Callable:
        if isinstance(type_obj, dict) or type_obj.endswith('yml') or type_obj.endswith('yaml'):
            return call(type_obj)
        if type_obj.endswith('json'):
            with open(file=type_obj, mode='r', encoding='UTF-8') as file:
                return call(json.loads(file.read()))

    return wrapper
