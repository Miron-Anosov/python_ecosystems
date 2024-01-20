from flask import Flask, request
from flask_restx import Api, Resource, fields
from marshmallow import ValidationError

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    delete_book_by_id,
    update_book_by_id,
    delete_author_by_id,
    get_author_by_id,
    add_author,
)
from schemas import (BookSchema,
                     BookIDValidator,
                     ValidatorExistsBook,
                     AuthorIDValidator,
                     AuthorSchema,
                     AuthorExistsValidator)

app = Flask(__name__)
api = Api(app, version='0.1.alpha', title="Books API", description='API for managing books')
api.default_namespace.name = 'Books'

author_model_body = api.model('Authors Body', {
    'first_name': fields.String(required=True, description='Authors first name'),
    'last_name': fields.String(required=True, description='Authors last name'),
    'middle_name': fields.String(required=False, description='Authors middle name'),
})

author_model_response = api.model('Author Response', {
    'author_id': fields.Integer(required=True, description='Authors ID'),
    'first_name': fields.String(required=True, description='Authors first name'),
    'last_name': fields.String(required=True, description='Authors last name'),
    'middle_name': fields.String(required=False, description='Authors middle name'),
})

book_model_response = api.model('Book Response', {
    'id': fields.Integer(required=True, description='Books ID'),
    'author_id': fields.Integer(required=True, description='Authors ID'),
    'title': fields.String(required=True, description='Authors ID'),
    'first_name': fields.String(required=True, description='Authors first name'),
    'last_name': fields.String(required=True, description='Authors last name'),
    'middle_name': fields.String(required=False, description='Authors middle name')
})

book_model_body_post = api.model('Book Body for PUT', {
    'title': fields.String(required=True, description='Books Title'),
    'first_name': fields.String(required=True, description='Authors first name'),
    'last_name': fields.String(required=True, description='Authors last name'),
    'middle_name': fields.String(required=False, description='Authors middle name')
})

book_model_body_patch = api.model('Book Body for PATCH', {
    'title': fields.String(required=False, description='Books Title'),
    'first_name': fields.String(required=False, description='Authors first name'),
    'last_name': fields.String(required=False, description='Authors last name'),
    'middle_name': fields.String(required=False, description='Authors middle name')
})


@api.route('/api/books')
class BookList(Resource):

    @api.doc(responses={200: 'Success', 400: 'Validation Error'}, model=book_model_response)
    def get(self) -> tuple[list[dict], int]:
        """Return all books."""
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    @api.expect(book_model_body_post)
    @api.doc(responses={201: 'Created', 400: 'Validation Error'}, model=book_model_response)
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


@api.route('/api/books/<int:id>')
class Book(Resource):
    """
    Класс дочерний от класса Resource.  Реализует методы для работы с книгами по их ID.
    """

    @api.expect(book_model_body_post)
    @api.doc(responses={204: 'No Content', 400: 'Validation Error', 201: 'Created'})
    def put(self, id: int) -> tuple:
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

    @api.doc(responses={200: 'Success', 400: 'Validation Error'}, model=book_model_response)
    def get(self, id: int) -> tuple:
        """ Return Book's JSON for ID. """
        try:
            schema_book_id = BookIDValidator()
            book_id: int = schema_book_id.load({'book_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            schema = BookSchema()
            return schema.dump(get_book_by_id(book_id), many=False), 200

    @api.doc(responses={204: 'No Content', 400: 'Validation Error'})
    def delete(self, id: int) -> tuple:
        """ Delete Book's JSON for ID."""
        try:
            schema_book_id = BookIDValidator()
            book_id = schema_book_id.load({'book_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            delete_book_by_id(book_id)
            return '', 204

    @api.expect(book_model_body_patch)
    @api.doc(responses={200: 'Success', 400: 'Validation Error'}, model=book_model_response)
    def patch(self, id: int) -> tuple:
        """ Update exist book. """
        data = request.json
        schema = BookSchema()
        schema_book_id = BookIDValidator()
        try:
            book_id = schema_book_id.load({'book_id': id})
            book = schema.load(data)
            book.id = book_id
        except ValidationError as exc:
            return exc.messages, 400
        else:
            book = update_book_by_id(book, return_book=True)
            return schema.dump(book), 200


@api.route('/api/authors/<int:id>', )
class Author(Resource):
    """
    Класс дочерний от класса Resource.  Реализует методы для работы с Авторами книг.
    """

    @api.doc(model=author_model_response, responses={200: 'Success', 400: 'Validation Error'})
    def get(self, id: int) -> tuple:
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

    @api.doc(responses={204: 'No Content', 400: 'Validation Error'})
    def delete(self, id: int) -> tuple:
        """ Delete author's data by ID and his books too."""
        schema_book_id = AuthorIDValidator()
        try:
            author_id = schema_book_id.load({'author_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            delete_author_by_id(author_id)
            return '', 204


@api.route('/api/authors/', )
class AuthorPost(Resource):
    """
    Класс дочерний от класса Resource.  Реализует методы для работы с Авторами книг.
    """

    @api.expect(author_model_body)
    @api.doc(model=author_model_response, responses={201: 'Created', 400: 'Validation Error'})
    def post(self) -> tuple:
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
    app.run(debug=True)
