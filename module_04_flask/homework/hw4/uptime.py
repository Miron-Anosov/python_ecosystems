"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""
import subprocess

from flask import Flask

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    """Endpoint предоставляет доступ к информации безпрерывной работы системы"""
    uptime_ = subprocess.run(['uptime', '-p'], capture_output=True, text=True).stdout
    return f"Current uptime is {uptime_}"


if __name__ == '__main__':
    app.run(debug=True)
