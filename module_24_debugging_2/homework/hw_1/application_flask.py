import sentry_sdk
from flask import Flask, jsonify

sentry_sdk.init(
    dsn="http://3d75643a25637f6c7305e719a78fd07c@127.0.0.1:9000/2",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # traces_sample_rate=1.0,
    # profiles_sample_rate=1.0,
    # enable_tracing=True
)

app = Flask(__name__)


@app.route(rule='/')
@app.route(rule='/status', methods=["GET", ])
def func() -> jsonify:
    return jsonify({'ok': 200})


@app.route(rule='/error')
def err():
    raise ZeroDivisionError('simple error')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
