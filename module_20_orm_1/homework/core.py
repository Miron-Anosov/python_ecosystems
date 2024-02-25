import json

from pydantic import ValidationError

from db_orm.coreORM import BooksORM, StudentsORM, ReceivingBooksORM
from validates_schema.ValidateModels import (BookSchema, StudentSchema, ReceivingBooksSchema,
                                             ReceivingBooksInputValidate,
                                             ErrorMessageSchema, ErrorMessageDetails,
                                             CollectionBooksSchema, CollectionStudentsSchema, TitleSchema,
                                             )


def get_all_books() -> json:
    """ Получение всех книг в библиотеке. """
    all_books_orm_obj_list = BooksORM().select_all_books()
    if all_books_orm_obj_list:
        books = [BookSchema.model_validate(book).model_dump() for book in all_books_orm_obj_list]
        return CollectionBooksSchema(books=books).model_dump_json()

    return ErrorMessageSchema(message='Библиотека пустая.').model_dump_json()


def get_student_who_did_not_return_book_within_14_days() -> json:
    """Получение список должников, которые держат книги у себя более 14 дней."""
    students_orm_obj_list = StudentsORM.select_students_who_late_more_two_weeks()
    if students_orm_obj_list:
        students = [StudentSchema.model_validate(student).model_dump()
                    for student in students_orm_obj_list]
        return CollectionStudentsSchema(students=students).model_dump_json()

    return ErrorMessageSchema(message='Должников в базе нет.').model_dump_json()


def give_the_book_from_library(student_id: int, book_id: int) -> json:
    """Выдать книгу студенту (POST - входные параметры ID книги и ID студента)"""
    try:
        ReceivingBooksInputValidate(student_id=student_id, book_id=book_id)
    except ValidationError as err:
        return ErrorMessageSchema(message=str(err),
                                  details=ErrorMessageDetails(student_id=student_id,
                                                              book_id=book_id
                                                              )
                                  ).model_dump_json()
    else:
        receive_book_orm_obj = ReceivingBooksORM.insert_give_books_to_student(student_id=student_id, book_id=book_id)
        if receive_book_orm_obj:
            return ReceivingBooksSchema.model_validate(receive_book_orm_obj, from_attributes=True).model_dump_json()

        return ErrorMessageSchema(message='Изменения не были применены. Данные в базе не будут сохранены',
                                  details=ErrorMessageDetails(student_id=student_id,
                                                              book_id=book_id
                                                              )
                                  ).model_dump_json()


def return_the_book_to_library(student_id: int, book_id: int) -> json:
    """
     Сдать книгу в библиотеку (POST - входные параметры ID книги и ID студента,
     в случае если такой связки нет, выдать ошибку)
    """
    try:
        ReceivingBooksInputValidate(student_id=student_id, book_id=book_id)
    except ValidationError as err:
        return ErrorMessageSchema(message=str(err),
                                  details=ErrorMessageDetails(student_id=student_id,
                                                              book_id=book_id
                                                              )
                                  ).model_dump_json()
    else:
        return_book_orm_obj = ReceivingBooksORM.update_return_book(student_id=student_id, book_id=book_id)
        if return_book_orm_obj:
            return ReceivingBooksSchema.model_validate(return_book_orm_obj, from_attributes=True).model_dump_json()

        return ErrorMessageSchema(message='Студента с такой книгой нет в базе.',
                                  details=ErrorMessageDetails(student_id=student_id,
                                                              book_id=book_id
                                                              )
                                  ).model_dump_json()


def get_book_by_title(title: str) -> json:
    """
        Усложнённое задание (по желанию) Создайте роут, с помощью которого будет осуществляться поиск книги по названию.
        На вход передается строка, по которой будет осуществляться поиск.
        Поиск должен выдавать книги, в названии которых содержится ключевая строка.
    """
    try:
        TitleSchema(title=title)
    except ValidationError as err:
        return ErrorMessageSchema(message=str(err)).model_dump_json()
    else:
        book_by_title_orm_obj = BooksORM.select_book_by_title(title_book=title)
        if book_by_title_orm_obj:
            return BookSchema.model_validate(book_by_title_orm_obj).model_dump_json(by_alias=True)

        return ErrorMessageSchema(message='Не найдено совпадений.').model_dump_json()
