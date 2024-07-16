from flask import Blueprint

coffe_route = Blueprint("coffeeshop", __name__, url_prefix="/coffeeshop")


@coffe_route.route(rule="/clients/", methods=["POST"])
def post_new_clients():
    """Добавление пользователя. В ответе должна быть информация по новому пользователю с его предпочтением по кофе"""
    ...


@coffe_route.route(rule="/look-for-coffee/", methods=["GET"])
def get_coffee_by_name():
    """Поиск кофе по названию (используйте полнотекстовый поиск, название — входной параметр)."""
    ...


@coffe_route.route(rule="/unic-items/", methods=["GET"])
def get_unique_items_in_notes_of_coffe():
    """Список уникальных элементов в заметках к кофе."""
    ...


@coffe_route.route(rule="/clients/", methods=["GET"])
def get_clients_in_intro_county():
    """Список пользователей, проживающих в стране (страна — входной параметр)."""
    ...
