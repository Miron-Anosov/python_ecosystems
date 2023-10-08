import datetime
from func_for_app import counter_func, word_from_book, car_output, cat_random_output

from flask import Flask

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    """Вывод приветствия."""
    return 'Hello world'


@app.route('/cars')
def cars():
    """Вывод списка автомобилей."""
    car = car_output()
    return f'Список машин: {car}'


@app.route('/cats')
def cats():
    """Вывод случайной породы кошек."""
    cat = cat_random_output()
    return f'Рандомный кот: {cat}'


@app.route('/get_time/now')
def get_time_now():
    """Вывод точного времени"""
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'«Точное время: {current_time}»'


@app.route('/get_time/future')
def get_time_future():
    """Вывод точного время через час"""
    current_time_after_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    return f'«Точное время через час будет {current_time_after_hour}»'


@app.route('/get_random_word')
def get_random_word():
    """Вывод случайного слова из книги"""
    word = word_from_book()
    return f'Одно рандомное слово из книги: {word}'


@app.route('/counter')
def counter():
    """Вывод счетчика вызова страницы"""
    count_run_func = counter_func()

    return f'Столько раз открывалась данная страница: {count_run_func}'


if __name__ == '__main__':
    app.run(debug=True)
