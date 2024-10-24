"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask
from manager_accounting import Manager

app = Flask(__name__)
manager = Manager()


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    return manager.add_date(date, number)


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    return manager.calculate_year_mouth(year)


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    return manager.calculate_year_mouth(year, month)


if __name__ == "__main__":
    app.run(debug=True)
