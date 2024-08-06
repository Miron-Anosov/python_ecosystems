import pytest  # noqa

from flask import Flask


from app.main import flask_maker_app


def test_type_app() -> None:
    app: Flask = flask_maker_app(testing=True, debug=True,
                                 host='127.0.0.1', port=5000)
    assert isinstance(app, Flask), "Type Error. Miss Flask obj"


def test_error_type_params() -> None:
    with pytest.raises(TypeError):
        _: Flask = flask_maker_app(testing=True, debug=True,
                                   host='127.0.0.1', port='')
