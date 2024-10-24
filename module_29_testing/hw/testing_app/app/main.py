from typing import Optional

from flask import Flask

from controllers import parking
from orm_models import db


def make_app(
    db_host_url: Optional[str] = None, testing: bool = False, debug: bool = False
) -> Flask:

    _app: Flask = Flask(__name__)
    _app.config["TESTING"] = testing
    _app.config["DEBUG"] = debug

    _app.config["SQLALCHEMY_DATABASE_URI"] = (
        db_host_url if db_host_url else "sqlite:///project.db"
    )

    _app.register_blueprint(parking)

    db.init_app(_app)

    _app.config["db"] = db

    with _app.app_context():
        db.create_all()

    return _app
