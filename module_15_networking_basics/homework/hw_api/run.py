from flask import Flask, request, jsonify

from module_15_networking_basics.homework.hw_api.data.database_interface import db_worker
from module_15_networking_basics.homework.hw_api.data.utils.json_worker import read_json

app = Flask(__name__)
db = db_worker()


@app.route('/room', methods=['GET'])
def room():
    if request.method == "GET":
        return jsonify(db.get_rooms()), 200


@app.route('/add-room', methods=['POST'])
def add_room():
    db.create_room(new_room=read_json(request.get_data().decode()))
    return jsonify(db.get_rooms()), 200


@app.route('/booking', methods=["POST"])
def booking():
    req = request.get_data().decode()
    if db.booking(person=read_json(req)):
        return "Can't book same room twice", 200  # TODO фраза, видимо, должна быть об успехе бронирования?
    return "Can't book same room twice", 409


if __name__ == '__main__':
    app.run(debug=True)
