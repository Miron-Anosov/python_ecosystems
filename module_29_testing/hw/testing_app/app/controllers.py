from flask import Blueprint, json, jsonify, request
from sqlalchemy import select
from orm_models import db, Client, Parking, ClientParking

parking = Blueprint("parking", __name__)


@parking.route("/clients", methods=["GET"])
def return_clients_from_db() -> json:
    """
    GET /clients — список всех клиентов.
    """
    list_clients = db.session.execute(select(Client)).scalars().all()

    list_dict_clients = []

    try:

        for client_from_db in list_clients:
            dict_client = {
                "name": client_from_db.name,
                "surname": client_from_db.surname,
                "credit card": f"*****{client_from_db.credit_card[-4:]}",  # very hard secret
                "car's number": client_from_db.car_number,
                "id": client_from_db.id
            }
            list_dict_clients.append(dict_client)

        return jsonify([{"clients": list_dict_clients}])

    except Exception:
        return jsonify({"Error": "Internal Server Error:"}), 500


@parking.route("/clients/<int:client_id>", methods=["GET"])
def return_client_by_id(client_id: int):
    """
    GET /clients/<client_id> — информация клиента по ID.

    Args:
        client_id (int): уникальное ID клиента.
    """
    try:
        assert isinstance(client_id, int), "miss client's id"
        client_from_db = db.get_or_404(Client, client_id)

        return jsonify([{'client': {
            "name": client_from_db.name,
            "surname": client_from_db.surname,
            "credit card": f"*****{client_from_db.credit_card[-4:]}",  # very hard secret
            "car's number": client_from_db.car_number,
            "id": client_from_db.id
        }}]), 200

    except AssertionError:
        return jsonify({"Error", "Bad Request"}), 400

    except Exception:
        return jsonify({"Error": "Internal Server Error:"}), 500


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
    try:
        if data := request.get_json():
            new_parking = Parking(**data)
            db.session.add(new_parking)
            db.session.flush()
            db.session.commit()

            return jsonify([{'parking': {
                "address": new_parking.address,
                "opened": new_parking.opened,
                "count places": new_parking.count_places,
                "count available places": new_parking.count_available_places,
                "id": new_parking.id
            }}]), 201

        return {"Error": "Bad request"}, 400

    except AttributeError:
        return jsonify({"Error": "Internal Server Error:"}), 500


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
