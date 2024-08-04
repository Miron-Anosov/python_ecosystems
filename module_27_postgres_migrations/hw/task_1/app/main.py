# import asyncpg
# import os
import logging
# import gunicorn
# from dotenv import load_dotenv
# from asyncpg import Pool
from flask import Flask, jsonify

app = Flask(__file__)

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


# load_dotenv()
# DB_KEY = 'DATABASE'
#
# db_host = os.getenv('POSTGRES_HOST')
# db_port = os.getenv('POSTGRES_PORT')
# db_user = os.getenv('POSTGRES_USER')
# db_database = os.getenv('POSTGRES_DB')
# db_password = os.getenv('POSTGRES_PASSWORD')
#
#
# @app.before_request
# async def connect_db():
#     logger.info('Создание пула подключений к БД')
#     pool: Pool = await asyncpg.create_pool(host=db_host,
#                                            port=db_port,
#                                            user=db_user,
#                                            database=db_database,
#                                            password=db_password,
#                                            min_size=6,
#                                            max_size=32)
#     app.config[DB_KEY] = pool


# @app.after_request
# async def close_connect_db():
#     logger.info('Закрытие пула подключений к БД')
#     pool: Pool = app.config[DB_KEY]
#     await pool.close()


@app.route("/", methods=["GET"])
def index():
    # volume = app.config[DB_KEY].execute('SELECT version();')
    # return jsonify({"database": volume})
    return jsonify({"database": 'volume'})

