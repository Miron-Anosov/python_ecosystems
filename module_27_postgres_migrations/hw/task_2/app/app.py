from flask import Flask
from controlers.coffeeshop import coffe_route

app = Flask(__name__)
app.register_blueprint(coffe_route)


@app.before_first_request
def init_data_for_db():
    """С помощью функции before_first_request создайте десять пользователей и десять сортов кофе."""
    ...


if __name__ == "__main__":
    app.run(host="", port=8000, debug=True)
