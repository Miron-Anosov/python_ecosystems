from sqlalchemy.exc import IntegrityError

import pytest

from .factories import (
    ClientFakeFactory,
    ParkingFakeFactory,
    ClientInvalidFakeFactory,
    ParkingInvalidFakeFactory,
    ClientParkingFakeFactory,
)
from app.orm_models import Client, Parking, ClientParking  # noqa


class TestCreateFakeDataToDB:
    def test_table_clients_is_empty(self, flask_app):
        with flask_app.app_context():
            client = flask_app.config["db"].session.get(Client, 1)
            assert client is None

    def test_create_clients(self, flask_app):
        with flask_app.app_context():
            new_client = ClientFakeFactory()
            flask_app.config["db"].session.commit()
            assert new_client.id is not None

    def test_get_clients_by_id(self, flask_app):
        with flask_app.app_context():
            client = flask_app.config["db"].session.get(Client, 1)
            assert client

    def test_invalid_client_model(self, flask_app):
        with pytest.raises(IntegrityError) as exc_info:
            with flask_app.app_context():
                new_client = ClientInvalidFakeFactory()
                print(new_client)
                flask_app.config["db"].session.commit()
                assert exc_info.type is IntegrityError

    def test_table_parking_is_empty(self, flask_app):
        with flask_app.app_context():
            parking = flask_app.config["db"].session.get(Parking, 1)
            assert parking is None

    def test_create_parking(self, flask_app):
        with flask_app.app_context():
            new_parking = ParkingFakeFactory()
            flask_app.config["db"].session.commit()
            assert new_parking.id is not None

    def test_get_parking_by_id(self, flask_app):
        with flask_app.app_context():
            parking = flask_app.config["db"].session.get(Parking, 1)
            assert parking

    def test_invalid_parking_model(self, flask_app):
        with pytest.raises(IntegrityError) as exc_info:
            with flask_app.app_context():
                ParkingInvalidFakeFactory()

                flask_app.config["db"].session.commit()
                assert exc_info.type is IntegrityError

    def test_table_client_parking_is_empty(self, flask_app):
        with flask_app.app_context():
            client_parking = flask_app.config["db"].session.get(ClientParking, 1)
            assert client_parking is None

    def test_create_client_parking(self, flask_app):
        with flask_app.app_context():
            new_client = ClientFakeFactory()
            new_parking = ParkingFakeFactory(opened=True)

            flask_app.config["db"].session.flush()

            new_client_parking = ClientParkingFakeFactory(
                client_id=new_client.id, parking_id=new_parking.id
            )

            flask_app.config["db"].session.flush()
            flask_app.config["db"].session.commit()
            assert new_client_parking.id is not None
