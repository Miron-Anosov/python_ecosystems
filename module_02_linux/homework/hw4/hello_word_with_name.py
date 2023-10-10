"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from datetime import datetime
from flask import Flask

app = Flask(__name__)


@app.route('/hello-world/<string:name_user>')
def hello_world(name_user: str):
    a = ("Хорошего Понедельника", "Хорошего Вторника", "Хорошей Среды", "Хорошего Четверга",
         "Хорошей Пятницы", 'Хорошей Субботы', "Хорошего Воскресенья")
    num_day = datetime.today().weekday()
    return f'Привет, {name_user}. {a[num_day]}!'


if __name__ == '__main__':
    app.run(debug=True)
