import pytest

from flask.testing import FlaskClient
from flask import Flask


from .factories import (
    ClientFakeFactory,
    ParkingFakeFactory,
)

from app.orm_models import Client, Parking, ClientParking  # noqa


class TestAPIandDB:

    def test_try_post_json_client_to_db(
        self, client_for_test_api_and_db: FlaskClient
    ) -> None:
        headers = {"Content-Type": "application/json"}
        params = {
            "name": "John",
            "surname": "Doe",
            "credit_card": "1234567812345678",
            "car_number": "XYZ1234",
        }
        response = client_for_test_api_and_db.post(
            "/clients", headers=headers, json=params
        )
        assert response.status_code == 201, "Params invalid"

    def test_get_clients(
        self, client_for_test_api_and_db: FlaskClient, flask_app: Flask
    ) -> None:

        dict_clients: int = 0
        url: str

        with flask_app.app_context():
            client: Client = ClientFakeFactory()
            flask_app.config["db"].session.commit()
            url = f"/clients/{client.id}"

        response = client_for_test_api_and_db.get(url)
        response_data_clients = response.get_json()[dict_clients]

        assert response.status_code == 200, "ID is now exists"
        assert response_data_clients.get("client").get("id") is not None

    def test_get_all_clients(self, client_for_test_api_and_db: FlaskClient) -> None:
        url: str = f"/clients"
        dict_clients: int = 0
        empty_db: int = 0

        response = client_for_test_api_and_db.get(url)

        assert response.status_code == 200

        list_clients: list = response.get_json()[dict_clients].get("clients")

        assert len(list_clients) > empty_db

    def test_post_parking_create(self, client_for_test_api_and_db: FlaskClient) -> None:
        headers = {"Content-Type": "application/json"}
        params = {
            "address": "123 Main St",
            "opened": False,
            "count_places": 100,
            "count_available_places": 80,
        }
        response = client_for_test_api_and_db.post(
            "/parkings", headers=headers, json=params
        )
        assert response.status_code == 201

    @pytest.fixture
    def test_post_client_parking_book_access(
        self, client: FlaskClient, flask_app: Flask
    ) -> dict:
        headers = {"Content-Type": "application/json"}

        with flask_app.app_context():

            client_fake = ClientFakeFactory(credit_card="77777777")
            parking_fake = ParkingFakeFactory(
                opened=True, count_places=10, count_available_places=9
            )
            flask_app.config["db"].session.commit()
            params = {"client_id": client_fake.id, "parking_id": parking_fake.id}

        response = client.post("/client_parkings", headers=headers, json=params)

        assert response.status_code == 201
        yield params

    def test_post_client_parking_book_fail_available_places_400(
        self, client: FlaskClient, flask_app: Flask
    ) -> None:
        headers = {"Content-Type": "application/json"}

        with flask_app.app_context():
            client_fake = ClientFakeFactory()
            parking_fake = ParkingFakeFactory(
                opened=True, count_places=10, count_available_places=0
            )
            flask_app.config["db"].session.commit()

            params = {"client_id": client_fake.id, "parking_id": parking_fake.id}

        response = client.post("/client_parkings", headers=headers, json=params)

        assert response.status_code == 400

    def test_post_client_parking_book_fail_opened_400(
        self, client: FlaskClient, flask_app: Flask
    ) -> None:
        headers = {"Content-Type": "application/json"}

        with flask_app.app_context():
            client_fake = ClientFakeFactory()
            parking_fake = ParkingFakeFactory(
                opened=False, count_places=10, count_available_places=9
            )
            flask_app.config["db"].session.commit()

            params = {"client_id": client_fake.id, "parking_id": parking_fake.id}

        response = client.post("/client_parkings", headers=headers, json=params)

        assert response.status_code == 400

    def test_delete_client_parking_access(
        self,
        client: FlaskClient,
        test_post_client_parking_book_access: dict,
    ) -> None:

        headers = {"Content-Type": "application/json"}
        response = client.delete(
            "/client_parkings",
            headers=headers,
            json=test_post_client_parking_book_access,
        )

        assert response.status_code == 202
