"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import subprocess
import shlex
from typing import List

from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    """"Endpoint предоставляет доступ к командам ps в терминале """
    args: List[str] = request.args.getlist("arg")
    command_str = " ".join(shlex.quote(str_) for str_ in args)
    command = shlex.split(command_str)
    command.insert(0, 'ps')
    print(command)
    result = subprocess.run(command, capture_output=True, text=True).stdout
    return f"<pre>{result}</pre>"
    # TODO для корректного отображения текста в формате html надо заменять символы <, >, и ":
    #  https://ruseller.com/lessons.php?rub=1&id=2106 иначе текст может отображаться не так как вы ожидаете,
    #  например часть текста отбрасывается или зачеркиваться т.д.


if __name__ == "__main__":
    app.run(debug=True)
