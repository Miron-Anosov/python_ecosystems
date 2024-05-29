import logging
import random
import time
from typing import Callable
from functools import wraps

from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
log = logging.getLogger(__name__)

metrics.info('flask_app', 'Backend server', version='0.1')

exs = ZeroDivisionError('simple error'), TimeoutError('timeout'), None, 0, []
endpoint_counter = metrics.counter(name='flask_app_counter', description='status code',
                                   labels={'path': lambda r: request.path,
                                           'method': lambda r: request.method,
                                           'host': lambda s: request.host,
                                           'args': lambda r: request.args,
                                           'user_agent': lambda r: request.user_agent,
                                           }
                                   )


def my_metrics(function: Callable) -> Callable:
    @wraps(function)
    @endpoint_counter
    def wrapper(*args, **kwargs) -> Callable:
        time.sleep(random.random())
        response = function(*args, **kwargs)
        return response
    return wrapper


@app.route(rule='/')
@app.route(rule='/main')
@my_metrics
def root_route() -> jsonify:
    ex_obj = random.choice(exs)
    if ex_obj:
        log.error(f"'/ fail {ex_obj}")
        raise ex_obj

    log.error("rule='/' running")
    return jsonify({'ok': 200})


@app.route(rule='/long-running')
@my_metrics
def something() -> jsonify:
    time.sleep(random.random())  # x2
    ex_obj = random.choice(exs)
    if ex_obj:
        log.error(f"'/long-running' fail {ex_obj}")
        raise ex_obj

    log.error("rule='/long-running' running")
    return jsonify({'OKe': 201}), 201


@app.route(rule='/test_error')
@my_metrics
def any_func() -> jsonify:
    ex_obj = random.choice(exs)
    if ex_obj:
        log.error(f"'/test_error' fail {ex_obj}")
        raise ex_obj

    log.error("'/test_error' do something")
    return jsonify({'Access': 200})


@app.errorhandler(TimeoutError)
@app.errorhandler(ZeroDivisionError)
@my_metrics
def err_zero(err):
    return jsonify({'error message': str(err)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
