import pytest

from flask.testing import FlaskClient
from flask import Flask
from flask import Response

from sqlalchemy.exc import IntegrityError

from .factories import (
    ClientFakeFactory,
    ParkingFakeFactory,
    ClientInvalidFakeFactory,
    ParkingInvalidFakeFactory,
    ClientParkingFakeFactory,
    ParkingFakeFactoryAlwaysOpened,
)

from app.orm_models import Client, Parking, ClientParking  # noqa


class TestAPIandDB:

    def test_get_clients(self, client_for_test_api_and_db: FlaskClient, flask_app: Flask):
        with flask_app.app_context():
            client: Client = ClientFakeFactory()
            flask_app.config["db"].session.commit()
            print(client)
        response = client_for_test_api_and_db.get(client.id)
        assert response.status_code == 200
