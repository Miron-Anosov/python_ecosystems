import psycopg2
import os
import logging

from dotenv import load_dotenv
from flask import Flask, jsonify, g

app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()

db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')
db_user = os.getenv('POSTGRES_USER')
db_database = os.getenv('POSTGRES_DB')
db_password = os.getenv('POSTGRES_PASSWORD')


def get_db_connection():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        dbname=db_database,
        password=db_password
    )


@app.before_request
def connect_db():
    logger.info('ПОДКЛЮЧЕНИЕ к БД')
    g.db_connection = get_db_connection()


@app.teardown_appcontext
def close_connect_db(exception):
    logger.info('ОТКЛЮЧЕНИЕ ОТ БД')
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()


@app.route("/", methods=["GET"])
def index():
    with g.db_connection.cursor() as cursor:
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        logger.info(f'{version=}')
    return jsonify({"database": version})


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('0.0.0.0', 8000, app)
