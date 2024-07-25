# Эндпоинты для работы с данными клиентов и кофе.

from typing import TYPE_CHECKING

from flask import Blueprint, request, jsonify
from ..models_orm import db_core
from ..validators import UserValidatorOutput, CoffeeValidatorOutput, UserValidatorInput
from pydantic import ValidationError

coffe_route = Blueprint("coffeeshop", __name__, url_prefix="/coffeeshop")

if TYPE_CHECKING:
    from ..models_orm.orm.user import UserORM  # noqa


@coffe_route.route(rule="/clients", methods=["POST"])
@db_core.with_session
def post_clients(db):
    """Добавление пользователя. В ответе должна быть информация по новому пользователю с его предпочтением по кофе"""
    data: dict = request.json
    try:
        validate_new_user: UserORM = db.insert_client(user_data=UserValidatorInput(**data).dict())
        return jsonify(UserValidatorOutput.model_validate(validate_new_user).model_dump()), 201
    except ValidationError as error:
        return jsonify(error.errors()), 422
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@coffe_route.route(rule="/look-for-coffee", methods=["GET"])
@db_core.with_session
def get_coffee_by_name(db):
    """Поиск кофе по названию (используйте полнотекстовый поиск, название — входной параметр)."""
    coffee_name: str = request.args.get('coffee_name', None)
    if not coffee_name:
        return jsonify({"error": "Parameter 'coffee_name' is required"}), 400

    try:
        coffees_by_name: list[dict] = [
            CoffeeValidatorOutput.model_validate(coffee).model_dump(by_alias=False)
            for coffee in db.select_coffee_by_name(type_coffee=coffee_name)
        ]

        return jsonify(coffees_by_name), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@coffe_route.route(rule="/unique-items", methods=["GET"])
@db_core.with_session
def get_unique_items_in_notes_of_coffe(db):
    """Список уникальных элементов в заметках к кофе."""
    try:
        return jsonify(db.select_unique_ingredients())
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@coffe_route.route(rule="/clients", methods=["GET"])
@db_core.with_session
def get_clients_by_country(db):
    """Список пользователей, проживающих в стране (страна — входной параметр)."""
    clients_from_same_country: str = request.args.get('country')
    if not clients_from_same_country:
        return jsonify({"error": "Parameter 'country' is required"}), 400

    try:
        clients = [UserValidatorOutput.model_validate(user).model_dump()
                   for user in db.select_clients_by_country(
                country=clients_from_same_country)]
        return jsonify(clients)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
