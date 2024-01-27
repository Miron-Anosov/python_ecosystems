from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, request
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger, swag_from
from flask_restful import Api, Resource
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
    add_author, Book,
)
from module_18_documentation.homework.hw1.API_flask_restful.swag_decor_util import swagger_doc_from_json_to_pydict
from module_18_documentation.homework.hw1.API_flask_restful.swagger_doc.author_del import author_del
from schemas import (BookSchema,
                     BookIDValidator,
                     ValidatorExistsBook,
                     AuthorIDValidator,
                     AuthorSchema,
                     AuthorExistsValidator, BookTypeValidate)

TITLE = 'API Library Books'
VERSION = '0.1.01.alpha'
OPENAPI_V = '2.0'
PREFIX = '/api'

app = Flask(__name__)
api = Api(app=app, prefix=PREFIX)

spec = APISpec(title=TITLE, version=VERSION, openapi_version=OPENAPI_V, plugins=[FlaskPlugin(), MarshmallowPlugin()], )
template = spec.to_flasgger(app, definitions=[BookSchema, AuthorSchema, ])
swagger = Swagger(app, template=template)


class BookList(Resource):

    @swag_from('swagger_doc/book_get.yml')
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    @swag_from('swagger_doc/book_post.yml')
    def post(self) -> tuple[dict, int]:
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


class BookObj(Resource):
    """
    Класс дочерний от класса Resource.  Реализует методы для работы с книгами по их ID.
    """

    @swag_from('swagger_doc/book_put_id.yml')
    def put(self, id: int) -> tuple[str, int]:
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

    @swag_from('swagger_doc/book_get_id.yml')
    def get(self, id: int) -> tuple[dict, int]:
        try:
            schema_book_id = BookIDValidator()
            book_id: int = schema_book_id.load({'book_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            schema = BookSchema()
            return schema.dump(get_book_by_id(book_id), many=False), 200

    @swag_from('swagger_doc/book_del_id.yml')
    def delete(self, id: int) -> tuple[str, int]:
        try:
            schema_book_id = BookIDValidator()
            book_id = schema_book_id.load({'book_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            delete_book_by_id(book_id)
            return '', 204

    @swag_from('swagger_doc/book_patch_id.yml')
    def patch(self, id: int) -> tuple[dict, int]:
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


swag_from = swagger_doc_from_json_to_pydict(swag_from)


class Author(Resource):
    """
    Класс дочерний от класса Resource.  Реализует методы для работы с Авторами книг.
    """

    @swag_from('swagger_doc/author_get.json')
    def get(self, id: int) -> tuple[dict, int]:
        schema = AuthorSchema()
        schema_book_id = AuthorIDValidator()
        try:
            author_id = schema_book_id.load({'author_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            author = get_author_by_id(author_id)
            return schema.dump(author), 200

    @swag_from(author_del)
    def delete(self, id: int) -> tuple[str, int]:
        schema_book_id = AuthorIDValidator()
        try:
            author_id = schema_book_id.load({'author_id': id})
        except ValidationError as exc:
            return exc.messages, 400
        else:
            delete_author_by_id(author_id)
            return '', 204


class AuthorPost(Resource):
    """
    Класс дочерний от класса Resource.  Реализует методы для работы с Авторами книг.
    """

    @swag_from('swagger_doc/author_post.json')
    def post(self) -> tuple[dict, int]:
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


api.add_resource(BookList, '/books')
api.add_resource(BookObj, '/books<int:id>')
api.add_resource(Author, '/authors/<int:id>')
api.add_resource(AuthorPost, '/authors')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
