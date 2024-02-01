from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace
from marshmallow import ValidationError
from werkzeug.serving import WSGIRequestHandler

from module_18_documentation.homework.hw1.API_flask_restx.models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    delete_book_by_id,
    update_book_by_id,
    delete_author_by_id,
    get_author_by_id,
    add_author, Book,
)
from module_18_documentation.homework.hw1.API_flask_restx.schemas import (
    BookSchema,
    BookIDValidator,
    ValidatorExistsBook,
    AuthorIDValidator,
    AuthorSchema,
    AuthorExistsValidator,
    BookTypeValidate)

app = Flask(__name__)
# app.config['SESSION_REFRESH_EACH_REQUEST'] = False
# app.config['TIMEOUT'] = 10
# app.config['KEEP_ALIVE_TIMEOUT'] = 30
# app.config['SERVER_NAME'] = '127.0.0.1:5000'


WSGIRequestHandler.protocol_version = "HTTP/1.1"
# WSGIRequestHandler.close_connection = False


with open('../README.md', 'r', encoding='UTF-8') as file:
    doc = file.read()

DESCRIPTION = "The API allows you to interact with database of books using HTTP protocols."
VERSION = '0.1.01.alpha'
TITLE = 'API Library Books'
PREFIX = '/api'
DOC_API_PATH = '/swagger'
DEFAULT = 'Library'
DEFAULT_LABEL = "Library of Books"
DEFAULT_SWAGGER_FILENAME = 'swagger_books_doc.json'
TERMS_URL = 'https://swagger.io/docs/specification/api-host-and-base-path/'

api = Api(app=app,
          version=VERSION,
          title=TITLE,
          description=doc,
          prefix=PREFIX,
          doc=DOC_API_PATH,
          default=DEFAULT,
          default_label=DEFAULT_LABEL,
          terms_url=TERMS_URL,
          default_swagger_filename=DEFAULT_SWAGGER_FILENAME,
          validate=True,
          )

books_group = Namespace('Books', "You can get data about some books or add new book in database.")
authors_group = Namespace('Authors', "You can get data about some authors or add new authors in database.")

api.add_namespace(authors_group, path='/authors')
api.add_namespace(books_group, path='/books')

author_model_body = api.model('Authors Body', {
    'first_name': fields.String(required=True, description='Authors first name', min_length=1, max_length=50,
                                default="Ivan"),
    'last_name': fields.String(required=True, description='Authors last name', min_length=2, max_length=50,
                               default="Ivanov"),
    'middle_name': fields.String(required=False, description='Authors middle name', min_length=0, max_length=50,
                                 default="Ivanovich"),
})

author_model_response = api.model('Author Response', {
    'author_id': fields.Integer(required=True, description='Authors ID'),
    'first_name': fields.String(required=True, description='Authors first name', min_length=1, max_length=50),
    'last_name': fields.String(required=True, description='Authors last name', min_length=2, max_length=50),
    'middle_name': fields.String(required=False, description='Authors middle name', min_length=0, max_length=50),
})

book_model_response = api.model('Book Response', {
    'id': fields.Integer(required=True, description='Books ID'),
    'author_id': fields.Integer(required=True, description='Authors ID'),
    'title': fields.String(required=True, description='Books name', min_length=1, max_length=350),
    'first_name': fields.String(required=True, description='Authors first name', min_length=1, max_length=50),
    'last_name': fields.String(required=True, description='Authors last name', min_length=2, max_length=50),
    'middle_name': fields.String(required=False, description='Authors middle name', min_length=0, max_length=50)
})

book_model_body_post = api.model('Book Body for PUT', {
    'title': fields.String(required=True, description='Books Title', min_length=1, max_length=350),
    'first_name': fields.String(required=True, description='Authors first name', min_length=1, max_length=50),
    'last_name': fields.String(required=True, description='Authors last name', min_length=2, max_length=50),
    'middle_name': fields.String(required=False, description='Authors middle name', min_length=0, max_length=50)
})

book_model_body_patch = api.model('Book Body for PATCH', {
    'title': fields.String(required=False, description='Books Title', min_length=1, max_length=350),
    'first_name': fields.String(required=False, description='Authors first name', min_length=1, max_length=50),
    'last_name': fields.String(required=False, description='Authors last name', min_length=2, max_length=50),
    'middle_name': fields.String(required=False, description='Authors middle name', min_length=0, max_length=50)
})


@books_group.route('', )
class BookList(Resource):
    GET_DESCRIPTION = 'You can get all book in the library'
    POST_DESCRIPTION = 'You can create new book in database.'

    @books_group.doc(responses={200: 'Success', 400: 'Validation Error'}, model=[book_model_response],
                     description=GET_DESCRIPTION)
    def get(self) -> tuple[list[dict], int]:
        """Return all books."""
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    @books_group.expect(book_model_body_post)
    @books_group.doc(responses={201: 'Created', 400: 'Validation Error'}, model=book_model_response,
                     description=POST_DESCRIPTION)
    def post(self) -> tuple[dict, int]:
        """Crate new book in Data."""
        data = request.json
        schema = BookSchema()
        book_valid = ValidatorExistsBook()
        data_title = {'title': data.get('title')}

        try:
            book_valid.load(data_title)
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        else:
            return schema.dump(add_book(book)), 201


@books_group.route('/<int:id>')
class BookObj(Resource):
    """
    Класс дочерний от класса Resource.  Реализует методы для работы с книгами по их ID.
    """
    DEL_DESCRIPTION = "This endpoint can delete some books in the database."
    PUT_DESCRIPTION = "This endpoint can create new book or update old book."
    GET_DESCRIPTION = "This endpoint can get you only one book by ID."
    PATCH_DESCRIPTION = ("This endpoint can  update info of book only.  "
                         "You can update a part of field or all fields.")

    @books_group.expect(book_model_body_post)
    @books_group.doc(responses={204: 'No Content', 400: 'Validation Error', 201: 'Created'},
                     description=PUT_DESCRIPTION)
    def put(self, id: int) -> tuple[str, int]:
        """ Update exist book or create new book. """
        data = request.json
        schema = BookSchema()
        schema_book_id = BookIDValidator()

        try:
            book_id = schema_book_id.load({'book_id': id})
            book = schema.load(data)
            book.id = book_id
            update_book_by_id(book)
            return '', 204
        except ValidationError:
            try:
                book = schema.load(data)
            except ValidationError as exc:
                return exc.messages, 400
            else:
                add_book(book)
                return '', 201

    @books_group.doc(responses={200: 'Success', 400: 'Validation Error'}, model=book_model_response,
                     description=GET_DESCRIPTION, )
    def get(self, id: int) -> tuple[dict, int]:
        """ Return Book's JSON for ID. """
        try:
            schema_book_id = BookIDValidator()
            book_id: int = schema_book_id.load({'book_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            schema = BookSchema()
            return schema.dump(get_book_by_id(book_id), many=False), 200

    @books_group.doc(responses={204: 'No Content', 400: 'Validation Error'}, description=DEL_DESCRIPTION,
                     deprecated=True)
    def delete(self, id: int) -> tuple[str, int]:
        """ Delete Book's JSON for ID."""
        try:
            schema_book_id = BookIDValidator()
            book_id = schema_book_id.load({'book_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            delete_book_by_id(book_id)
            return '', 204

    @books_group.expect(book_model_body_patch)
    @books_group.doc(responses={200: 'Success', 400: 'Validation Error'}, model=book_model_response,
                     description=PATCH_DESCRIPTION)
    def patch(self, id: int) -> tuple[dict, int]:
        """ Update exist book. """
        data = request.json
        schema = BookSchema()
        valid_book_id = BookIDValidator()
        field_valid = BookTypeValidate()
        try:
            book_id = valid_book_id.load({'book_id': id})
            up_data = field_valid.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        else:
            book_old: Book = get_book_by_id(book_id)
            for field, data in up_data.items():
                setattr(book_old, field, data)
            book = update_book_by_id(book_old, return_book=True)
            return schema.dump(book), 200


@authors_group.route('/<int:id>', )
class Author(Resource):
    """
    Класс дочерний от класса Resource.  Реализует методы для работы с Авторами книг.
    """
    GET_DESCRIPTION = "You can get an author by ID"
    DELETE_DESCRIPTION = "You can delete an author by ID, and the author's books will be deleted as well."

    @authors_group.doc(model=author_model_response, responses={200: 'Success', 400: 'Validation Error'},
                       description=GET_DESCRIPTION)
    def get(self, id: int) -> tuple[dict, int]:
        """ Return author's data by ID"""
        schema = AuthorSchema()
        schema_book_id = AuthorIDValidator()
        try:
            author_id = schema_book_id.load({'author_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            author = get_author_by_id(author_id)
            return schema.dump(author), 200

    @authors_group.doc(responses={204: 'No Content', 400: 'Validation Error'}, description=DELETE_DESCRIPTION)
    def delete(self, id: int) -> tuple[str, int]:
        """ Delete author's data by ID and his books too."""
        schema_book_id = AuthorIDValidator()
        try:
            author_id = schema_book_id.load({'author_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            delete_author_by_id(author_id)
            return '', 204


@authors_group.route('')
class AuthorPost(Resource):
    """
    Класс дочерний от класса Resource.  Реализует методы для работы с Авторами книг.
    """
    POST_DESCRIPTION = "You can create an author in the database by providing their first name and last name."

    @authors_group.expect(author_model_body)
    @authors_group.doc(model=author_model_response, responses={201: 'Created', 400: 'Validation Error'},
                       description=POST_DESCRIPTION)
    def post(self) -> tuple[dict, int]:
        """Create new author."""
        data_author = request.json
        schema = AuthorSchema()
        author_check = AuthorExistsValidator()

        try:
            author_check.load(data_author)
            author = schema.load(data_author)
        except ValidationError as exc:
            return exc.messages, 400
        else:
            author = add_author(author)
            return schema.dump(author), 201


if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True, threaded=True)
