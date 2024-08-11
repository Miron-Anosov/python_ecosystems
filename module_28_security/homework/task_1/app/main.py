from typing import TYPE_CHECKING

from flask import Flask, jsonify, request

if TYPE_CHECKING:
    from flask import Response  # noqa

from flask_cors import CORS

ORIGIN = "https://www.google.com"

app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": [ORIGIN],
    "methods": ["GET", "POST"],
    "allow_headers": ['Content-Type', 'X-My-Fancy-Header']
}})


@app.route('/', methods=['GET', 'POST'])
def handler():
    print(request.headers)

    if request.method == "POST":
        data = request.json
        print(data)
        return jsonify({"Data": data})

    return jsonify({"Hello": "User"})


# @app.after_request
# def add_cors(response: Response):
#     """Не забудьте сделать это через декоратор, который мы разобрали ранее."""
#     response.headers['Access-Control-Allow-Origin'] = ORIGIN
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST"
#     response.headers["Access-Control-Allow-Headers"] = "X-My-Fancy-Header, Content-Type"
#     return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)
