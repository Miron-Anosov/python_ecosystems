import datetime

from flask import Blueprint, json, jsonify, request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from orm_models import db, Client, Parking, ClientParking

parking = Blueprint("parking", __name__)


@parking.route("/clients", methods=["GET"])
def return_clients_from_db() -> json:
    """
    GET /clients — список всех клиентов.
    """
    list_clients = db.session.execute(select(Client)).scalars().all()

    list_dict_clients = []

    for client_from_db in list_clients:
        dict_client = {
            "name": client_from_db.name,
            "surname": client_from_db.surname,
            "credit card": f"{''.join(
                '*****' + client_from_db.credit_card[-4:]) if client_from_db.credit_card else None}",
            "car's number": client_from_db.car_number,
            "id": client_from_db.id,
        }
        list_dict_clients.append(dict_client)

    return jsonify([{"clients": list_dict_clients}])


@parking.route("/clients/<int:client_id>", methods=["GET"])
def return_client_by_id(client_id: int) -> json:
    """
    GET /clients/<client_id> — информация клиента по ID.

    Args:
        client_id (int): уникальное ID клиента.
    """

    client_from_db = db.get_or_404(Client, client_id)

    return (
        jsonify(
            [
                {
                    "client": {
                        "name": client_from_db.name,
                        "surname": client_from_db.surname,
                        "credit card": f"{''.join(
                             '*****' + client_from_db.credit_card[-4:]) if client_from_db.credit_card else None}",
                        "car's number": client_from_db.car_number,
                        "id": client_from_db.id,
                    }
                }
            ]
        ),
        200,
    )


@parking.route("/clients", methods=["POST"])
def make_client():
    """
    POST /clients — создать нового клиента.

    Notes
         curl -X POST http://localhost:8080/clients \
             -H "Content-Type: application/json" \
             -d '{
                       "name": "John",
                       "surname": "Doe",
                       "credit_card": "1234567812345678",
                       "car_number": "XYZ1234"
                     }'
    """
    try:
        data = request.get_json()
        client = Client(**data)
        db.session.add(client)
        db.session.flush()
        db.session.commit()

        return (
            jsonify(
                [
                    {
                        "client": {
                            "name": client.name,
                            "surname": client.surname,
                            "credit card": f"{''.join(
                                '*****' + client.credit_card[-4:]) if client.credit_card else None}",
                            "car's number": client.car_number,
                            "id": client.id,
                        }
                    }
                ]
            ),
            201,
        )

    except IntegrityError:
        return jsonify({"Error": f"Bad request"}), 400


@parking.route("/parkings", methods=["POST"])
def make_parking():
    """
    POST /parkings — создать новую парковочную зону.

    Notes:
        curl -X POST http://localhost:8080/parkings \
             -H "Content-Type: application/json" \
             -d '{
                   "address": "123 Main St",
                   "opened": false,
                   "count_places": 100,
                   "count_available_places": 80
                 }'
    """
    try:
        data = request.get_json()
        new_parking = Parking(**data)
        db.session.add(new_parking)
        db.session.flush()
        db.session.commit()

        return (
            jsonify(
                [
                    {
                        "parking": {
                            "address": new_parking.address,
                            "opened": new_parking.opened,
                            "count places": new_parking.count_places,
                            "count available places": new_parking.count_available_places,
                            "id": new_parking.id,
                        }
                    }
                ]
            ),
            201,
        )

    except IntegrityError:
        return jsonify({"Error": f"Bad request"}), 400


@parking.route("/client_parkings", methods=["POST"])
def go_to_parking_place() -> json:
    """
    POST client_parkings — заезд на парковку (проверить, открыта ли парковка,
    количество свободных мест на парковке уменьшается, фиксируется дата заезда)
    В теле запроса передать client_id, parking_id.

    Notes:
        curl -X POST http://localhost:8080/client_parkings \
             -H "Content-Type: application/json" \
             -d '{
                   "client_id": 1,
                   "parking_id": 1
                 }'
    """
    book_place: int = 1
    not_enough_parking_places: int = 0

    try:
        data = request.get_json()

        parking_try = ClientParking(**data)
        parking_from_db = db.session.get(Parking, parking_try.parking_id)

        assert parking_from_db.opened is True, "Parking probably is close"
        assert (
            parking_from_db.count_available_places > not_enough_parking_places
        ), "Parking hasn't free place"

        parking_from_db.count_available_places -= book_place
        parking_try.time_in = datetime.datetime.now(datetime.timezone.utc)

        db.session.add(parking_try)
        db.session.flush()
        db.session.commit()

        return (
            jsonify(
                [
                    {
                        "book parking place": {
                            "client id": parking_try.client_id,
                            "parking id": parking_try.parking_id,
                            "time in": parking_try.time_in,
                            "time out": parking_try.time_out,
                            "id": parking_try.id,
                        }
                    }
                ]
            ),
            201,
        )

    except (IntegrityError, TypeError, AttributeError, AssertionError):
        return jsonify({"Error": f"Bad request"}), 400


@parking.route("/client_parkings", methods=["DELETE"])
def go_out_from_parking_place() -> json:
    """
    DELETE client_parkings — выезд с парковки (количество свободных мест
    увеличивается проставляем время выезда).
    В теле запроса передать client_id, parking_id.

    Notes:
        curl -X DELETE http://localhost:8080/client_parkings \
     -H "Content-Type: application/json" \
     -d '{
           "client_id": 1,
           "parking_id": 1
         }'

    """
    book_place: int = 1

    try:
        data = request.get_json()
        client_id, parking_id = data.get("client_id"), data.get("parking_id")

        try_go_out_from_parking = db.session.execute(
            select(ClientParking)
            .where(ClientParking.parking_id == parking_id)
            .where(ClientParking.client_id == client_id)
        ).scalar_one()

        parking_place = db.session.get(Parking, parking_id)

        parking_place.count_available_places += book_place

        client = db.session.get(Client, client_id)

        assert client.credit_card is not None, "The client does not have a credit card."
        assert parking_place.count_available_places <= parking_place.count_places, (
            f"The parking is empty! available_places={parking_place.count_available_places}, "
            f"count_places{parking_place.count_places}"
        )

        try_go_out_from_parking.time_out = datetime.datetime.now(datetime.timezone.utc)

        db.session.flush()
        db.session.commit()

        return (
            jsonify(
                [
                    {
                        "leave parking place": {
                            "client id": try_go_out_from_parking.client_id,
                            "parking id": try_go_out_from_parking.parking_id,
                            "time in": try_go_out_from_parking.time_in,
                            "time out": try_go_out_from_parking.time_out,
                            "id": try_go_out_from_parking.id,
                        }
                    }
                ]
            ),
            202,
        )

    except (
        NoResultFound,
        TypeError,
        AssertionError
    ):
        return jsonify({"Error": f"Bad request"}), 400
