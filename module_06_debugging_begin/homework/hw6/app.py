"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""
from typing import List, Any

from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'


@app.route('/about/<site>', defaults={'site': 'Skillbox'})
def about(site: str):
    return f'about {site}'


@app.errorhandler(404)
def not_found(error: 404):
    """
    Функция вызывается в случае возникновения ошибки 404 и возвращает список доступных маршрутов.
    """
    title: str = 'The requested URL was not found on the server'
    # Формируем список доступных маршрутов.
    links: List[tuple[str, Any]] = []
    for rule in app.url_map.iter_rules():
        # Проверяем наличие аргументов.
        arguments: str = rule.arguments if rule.arguments is not None else ()
        # Проверяем наличие параметров по умолчанию у аргументов, если таковых нет,
        # то переход по маршруту будет недоступен.
        defaults: str = rule.defaults if rule.defaults is not None else ()
        # добавляем только те страницы, по которым можно перейти.
        if "GET" in rule.methods and len(defaults) >= len(arguments):
            # Формируем маршрут, при наличии параметров, они будут так же переданы.
            url: str = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))  # Передаем маршрут и название эндпоинта.
    return render_template(template_name_or_list='all_links.html', links=links, title=title, h6=title), 404


if __name__ == '__main__':
    app.run(debug=True)
