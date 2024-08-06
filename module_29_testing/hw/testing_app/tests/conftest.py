import pytest

from typing import Generator

from flask import Flask

from app.main import make_app


@pytest.fixture()
def flask_app() -> Generator[Flask, None, None]:
    app = make_app(testint=True, host='127.0.0.1', port=5000)
    
    yield app
    app.teardown_appcontext()


@pytest.fixture()
def client(flask_app: Flask) -> Flask:
    return flask_app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
