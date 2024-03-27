from flask import Flask, json, request

from module_21_orm_2.homework.db_orm.models.modelsORM import create_all_tables
from module_21_orm_2.homework.core import (
    get_all_books,
    get_student_who_did_not_return_book_within_14_days, give_the_book_from_library, return_the_book_to_library,
    get_book_by_title, count_books_by_authors, get_books_by_authors_that_is_not_read,
    get_avg_books_on_the_current_mouth, get_top_book, get_top_student, make_file_csv,
    make_students_validate_models_from_csv_file, post_models_to_db)

app = Flask(__name__)


@app.before_request
def create_library_tables() -> None:
    create_all_tables()


@app.route('/books/', methods=['GET', 'POST'])
def get_books() -> json:
    if request.method == 'POST':
        return get_book_by_title(**request.json)
    return get_all_books()


@app.route('/students/', methods=['GET', 'POST'])
def get_students() -> json:
    if request.method == 'POST':
        return get_books_by_authors_that_is_not_read(**request.json)
    return get_student_who_did_not_return_book_within_14_days()


@app.route('/receiving/', methods=['GET', 'POST'])
def give_the_book() -> json:
    if request.method == 'POST':
        return give_the_book_from_library(**request.json)
    return get_avg_books_on_the_current_mouth()


@app.route('/transfer/', methods=['POST'])
def return_books() -> json:
    return return_the_book_to_library(**request.json)


@app.route('/authors/', methods=['GET'])
def authors_and_count_books() -> json:
    return count_books_by_authors()


@app.route('/top-chart/book/', methods=['GET'])
def get_top_book_() -> json:
    return get_top_book()


@app.route('/top-chart/student/', methods=['GET'])
def get_top_student_() -> json:
    return get_top_student()


@app.route('/upload/', methods=['GET', "POST"])
def read_scv_file() -> json:
    """Создайте роут, который будет принимать csv-файл с данными по студентам (разделитель ;)."""
    if 'file' not in request.files:
        return json.dumps({'The file was empty': None})

    if file := request.files.get('file'):

        filename = file.filename
        make_file_csv(text_csv=file.stream.read(), filename=filename)
        models = make_students_validate_models_from_csv_file(filename=filename)
        post_models_to_db(models.get('students'))

        if models.get('errors'):
            return json.dumps({'The list of students was loaded ': models.get('errors')})

        return json.dumps({'The list of students was loaded ': True})

    return json.dumps({'The file was empty': None})


if __name__ == '__main__':
    app.secret_key = '0000'
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
