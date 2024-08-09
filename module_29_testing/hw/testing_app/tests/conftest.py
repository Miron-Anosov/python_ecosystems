import pytest

from typing import Generator

from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from app.main import make_app  # noqa


@pytest.fixture(scope="session")
def flask_app() -> Generator[Flask, None, None]:
    host_db = "sqlite:///test.db"
    app: Flask = make_app(db_host_url=host_db, testing=True, debug=True)

    yield app

    with app.app_context():
        app.config["db"].drop_all()


@pytest.fixture(scope="session")
def client(flask_app: Flask) -> FlaskClient:
    yield flask_app.test_client()


@pytest.fixture(scope="function")
def client_scope_only_func(flask_app: Flask) -> FlaskClient:
    yield flask_app.test_client()


@pytest.fixture(scope="session")
def runner(flask_app) -> FlaskCliRunner:
    yield flask_app.test_cli_runner()


@pytest.fixture(scope="module")
def get_all_client_response(client: FlaskClient):
    yield client.get("/clients")


@pytest.fixture(scope="module")
def get_client_by_id_response(client: FlaskClient):
    yield client.get("/clients/1")
