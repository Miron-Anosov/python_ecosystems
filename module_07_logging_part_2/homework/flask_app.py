import logging
from typing import List
from flask import Flask, request
from app import base_config_log

base_config_log()
logger: logging.Logger = logging.getLogger('flask')
app: Flask = Flask(__name__)

data_logs: List[str] = []


@app.route('/log/', methods=['POST'])
def log() -> tuple[str, int]:
    log_str: str = ''
    for _, value in request.form.items():
        if len(log_str) == 0:
            log_str: str = ''.join(f"{value}")
        else:
            log_str: str = ''.join(f"{log_str}{' | '}{value}")
    data_logs.append(log_str)
    logger.info(f"A new log added in the data_logs. Them is already an amount: {len(data_logs)}")
    return 'OK', 200


@app.route('/logs/', methods=['GET'])
def show_logs() -> tuple[str, int]:
    if data_logs:
        logger.info(f'Logs returns an amount: {len(data_logs)}')
        return '<br>'.join(line for line in data_logs), 200
    return "empty", 200


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True, port=3000)
