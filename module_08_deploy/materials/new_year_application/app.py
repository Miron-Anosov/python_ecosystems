import os

from flask import Flask, render_template

root_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, )


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
