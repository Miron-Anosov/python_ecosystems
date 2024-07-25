# Основной модуль.

from flask import Flask
from core import coffe_route
from core.models_orm import create_data

app = Flask(__name__)
app.register_blueprint(coffe_route)


@app.before_first_request
def init_data_for_db():
    """
    С помощью функции before_first_request создайте десять пользователей и десять сортов кофе.
    """
    create_data()


if __name__ == "__main__":
    app.run(host="", port=8000, debug=True)
