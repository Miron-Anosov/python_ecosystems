from flask import Flask, render_template, request, redirect, url_for
# from typing import List
from flask import Response

from models import init_db, get_all_books, DATA, add_book_in_table, search_author
from form_book_validate import BookForm, SearchAuthor

app: Flask = Flask(__name__)


# def _get_html_table_for_books(books: List[dict]) -> str:
#     table = """
# <table>
#     <thead>
#     <tr>
#         <th>ID</td>
#         <th>Title</td>
#         <th>Author</td>
#     </tr>
#     </thead>
#     <tbody>
#         {books_rows}
#     </tbody>
# </table>
# """
#     rows: str = ''
#     for book in books:
#         rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
#             id=book['id'], title=book['title'], author=book['author'],
#         )
#     return table.format(books_rows=rows)


@app.route('/books/')
def all_books() -> str:
    return render_template('index.html', books=get_all_books())


@app.route('/books/form/', methods=['GET', 'POST'])
def get_books_form() -> str | Response:
    if request.method == 'GET':
        return render_template('add_book.html')
    elif request.method == 'POST':
        form_book = BookForm()
        if form_book.validate_on_submit():
            author, title = form_book.author_name.data, form_book.book_title.data
            add_book_in_table(title=title, author=author)
    return redirect(url_for('all_books'))


@app.route('/books/search/', methods=['GET', "POST"])
def search_books() -> str | Response:
    if request.method == "GET":
        return render_template('search_books.html')
    elif request.method == "POST":
        search_books_form = SearchAuthor()
        if search_books_form.validate_on_submit():
            author: str = search_books_form.search.data
            print(author)
            return render_template('found_authors_books.html', books=search_author(author), author=author)
        return render_template('found_authors_books.html')


@app.route('/books/id/')
def return_books_id_and_count_view() -> str:
    return render_template("books_id.html", books=get_all_books(True))


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    init_db(DATA)
    app.run(debug=True)
