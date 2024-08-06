from flask import Blueprint, json, jsonify, request
from orm_models import db, Client

parking = Blueprint("parking", __name__)


@parking.route("/clients", methods=["GET"])
def return_clients_from_db() -> json:
    """
    GET /clients — список всех клиентов.
    """
    return jsonify({"test": "OK"})


@parking.route("/clients/<int:client_id>", methods=["GET"])
def return_client_by_id(client_id: int):
    """
    GET /clients/<client_id> — информация клиента по ID.

    Args:
        client_id (int): уникальное ID клиента.
    """
    return jsonify({"client_id": client_id})


@parking.route("/clients", methods=["POST"])
def make_client():
    """
    POST /clients — создать нового клиента.
    """
    if data := request.get_json():
        client = Client(**data)
        print(client)
        client_db = db.session.add(client)

        print(client_db)


@parking.route("/parkings", methods=["POST"])
def make_parking():
    """
    POST /parkings — создать новую парковочную зону.
    """
    ...


@parking.route("/client_parkings", methods=["POST"])
def go_to_parking_place() -> json:
    """
    POST client_parkings — заезд на парковку (проверить, открыта ли парковка,
    количество свободных мест на парковке уменьшается, фиксируется дата заезда)
    В теле запроса передать client_id, parking_id.
    """
    ...


@parking.route("/client_parkings")
def go_out_from_parkin_place() -> json:
    """
    DELETE client_parkings — выезд с парковки (количество свободных мест
    увеличивается проставляем время выезда).
    В теле запроса передать client_id, parking_id.
    """
    ...
