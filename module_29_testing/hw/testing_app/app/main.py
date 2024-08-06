from typing import Optional

from flask import Flask

from controllers import parking
from orm_models import db


def make_app(db_host_url: Optional[str] = None, testing: bool = False,
             debug: bool = False) -> Flask:

    app: Flask = Flask(__name__)
    app.config["TESTING"] = testing
    app.config["DEBUG"] = debug

    app.config["SQLALCHEMY_DATABASE_URI"] = db_host_url \
        if db_host_url else "sqlite:///project.db"

    app.register_blueprint(parking)

    db.init_app(app)

    # with app.app_context():
    #     db.create_all()

    return app


if __name__ == "__main__":
    app = make_app(debug=True)
    with app.app_context():
        db.create_all()
        db.session.commit()

    app.run(host="0.0.0.0", port=8080)
