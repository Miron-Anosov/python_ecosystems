from flask import Flask, json, request

from module_20_orm_1.homework.core import (
    get_all_books,
    get_student_who_did_not_return_book_within_14_days, give_the_book_from_library, return_the_book_to_library,
    get_book_by_title, )

app = Flask(__name__)


@app.route('/books/', methods=['GET'])
def get_all_books_() -> json:
    return get_all_books()


@app.route('/books/', methods=['POST'])
def get_book_by_title_():
    return get_book_by_title(**request.json)


@app.route('/students/', methods=['GET'])
def get_student_who_did_not_return_book() -> json:
    return get_student_who_did_not_return_book_within_14_days()


@app.route('/receiving/', methods=['POST'])
def give_the_book() -> json:
    return give_the_book_from_library(**request.json)


@app.route('/transfer/', methods=['POST'])
def return_books() -> json:
    return return_the_book_to_library(**request.json)


if __name__ == '__main__':
    app.run(debug=True)
