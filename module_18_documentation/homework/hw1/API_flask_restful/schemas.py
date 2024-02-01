from flasgger import Schema, fields, ValidationError
from marshmallow import validates, post_load, validates_schema

from module_18_documentation.homework.hw1.API_flask_restful.models import (
    check_book,
    Book,
    get_truth_book_id,
    get_truth_author_id,
    Author,
    check_author_in_bd
)


class BookSchema(Schema):
    """Сериализатор/Десериализатор Книги"""
    id = fields.Int(dump_only=True)
    author_id = fields.Int(required=False)
    title = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)

    @post_load
    def create_book(self, data: dict, **_) -> Book:
        return Book(**data)


class AuthorSchema(Schema):
    """Сериализатор/Десериализатор Автора"""
    author_id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)

    @post_load
    def create_author(self, data: dict, **_) -> Author:
        return Author(**data)


class BookIDValidator(Schema):
    """Валидатор ID книги"""
    book_id = fields.Int(required=True)

    @validates('book_id')
    def validate_book_id(self, book_id: int) -> None:
        if not get_truth_book_id(book_id):
            raise ValidationError(f'Invalid book_id: {book_id}. Book does not exist.')

    @post_load
    def return_book_id(self, data: dict, **_) -> int:
        return data.get('book_id')


class ValidatorExistsBook(Schema):
    """Валидатор названия книги."""
    title = fields.Str(required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if check_book(title) is not None:
            raise ValidationError(f"Book with title '{title}' already exists, please use a different title.")


class AuthorIDValidator(Schema):
    """Валидатор ID Автора. Проверяется его наличие в БД."""
    author_id = fields.Int(required=True)

    @validates('author_id')
    def validate_title(self, author_id: int) -> None:
        if get_truth_author_id(author_id) is None:
            raise ValidationError(f"Author with ID: '{author_id}' is not exists.")

    @post_load
    def return_author_id(self, data: dict, **_) -> int:
        return data.get('author_id')


class AuthorExistsValidator(Schema):
    """"Валидотор Автора. Проверяется его наличие в БД."""
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)

    @validates_schema
    def validate_title(self, author_data, **_) -> None:
        if check_author_in_bd(**author_data):
            raise ValidationError(f"Author with data '{author_data}' already exists, please use a different data.")


class BookTypeValidate(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=False)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    middle_name = fields.Str(required=False)

    @post_load
    def return_valid_type(self, data: dict, **_):
        return data
