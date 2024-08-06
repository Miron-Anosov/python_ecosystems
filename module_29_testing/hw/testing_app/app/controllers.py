from flask import Blueprint, json, jsonify, request
from sqlalchemy import insert, select
from orm_models import db, Client, Parking, ClientParking

parking = Blueprint("parking", __name__)


@parking.route("/clients", methods=["GET"])
def return_clients_from_db() -> json:
    """
    GET /clients — список всех клиентов.
    """
    list_clients = db.session.execute(select(Client)).scalars().all()
    print(list_clients)
    return list_clients


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
    try:
        if data := request.get_json():
            client = Client(**data)
            db.session.add(client)
            db.session.flush()
            db.session.commit()

            return jsonify([{'client': {
                "name": client.name,
                "surname": client.surname,
                "credit card": f"*****{client.credit_card[-4:]}",  # very hard secret
                "car's number": client.car_number,
                "id": client.id
            }}]), 201

        return {"Error": "Bad request"}, 400

    except AttributeError:
        return jsonify({"Error": "Internal Server Error:"}), 500


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
