import operator

from flask import Flask
from flask_jsonrpc import JSONRPC
from flasgger import Swagger
from flask_jsonrpc.exceptions import InvalidParamsError

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

swagger = Swagger(app, template_file='template/swagger.yml')


@jsonrpc.method('calc.add')
def add(a: float | int, b: float | int) -> float | int:
    return operator.add(a, b)


@jsonrpc.method('calc.sub')
def minus(a: float | int, b: float | int) -> float | int:
    return operator.sub(a, b)


@jsonrpc.method('calc.mul')
def mul(a: float | int, b: float | int) -> float | int:
    return operator.mul(a, b)


@jsonrpc.method('calc.div')
def div(a: float | int, b: float | int) -> float | int:
    try:
        return operator.floordiv(a, b)
    except Exception:
        raise InvalidParamsError


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
