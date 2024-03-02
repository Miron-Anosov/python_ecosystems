import json
import csv
from typing import Any

from pydantic import ValidationError

from module_21_orm_2.homework.db_orm.coreORM import BooksORM, StudentsORM, ReceivingBooksORM
from validates_schema.ValidateModels import (BookSchema, StudentSchema, ReceivingBooksSchema,
                                             ReceivingBooksInputValidate,
                                             ErrorMessageSchema, ErrorMessageDetails,
                                             CollectionBooksSchema, CollectionStudentsSchema, TitleSchema,
                                             AuthorsCollectionSchema, AuthorsSchema,
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
        return CollectionStudentsSchema(students=students).model_dump_json(exclude_none=True)

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


def count_books_by_authors() -> json:
    """Получить кол-во оставшихся в библиотеке книг по автору (GET -входной параметр - ID автора)"""
    list_authors = [AuthorsSchema(id=model_orm.id,
                                  name=model_orm.name,
                                  surname=model_orm.surname,
                                  count_books=model_orm.count_books,
                                  )
                    .model_dump() for model_orm in
                    BooksORM.select_count_books_by_authors()
                    ]

    return AuthorsCollectionSchema(authors=list_authors).json(exclude_none=True)


def get_books_by_authors_that_is_not_read(id_student: int) -> json:
    """
    Получить список книг, которые студент не читал, при этом другие книги этого автора студент уже брал
    (GET - входной параметр - ID студента). Пример: Я брал книгу Льва Толстого “Война и мир”,
    роут должен вернуть другие произведения этого автора, которые есть в библиотеке.

    #TODO как понимать другие произведения автора, если по заданию мы выборку делаем по студенту?
    #TODO Может тогда идет речь не об авторе, а обо всех авторах?
    #TODO  Не понятно каким образом мне решать какого автора возвращать.
    """

    books = [
        BookSchema.model_validate(book_orm) for book_orm in
        StudentsORM.select_book_by_authors_that_is_not_read(id_student=id_student)
    ]
    if books:
        return CollectionBooksSchema(books=books).model_dump_json()
    return ErrorMessageSchema(message='Не найдено совпадений.').model_dump_json()


def get_avg_books_on_the_current_mouth() -> json:
    """Получить среднее кол-во книг, которые студенты брали в этом месяце (GET)"""
    if float_res := ReceivingBooksORM.select_avg_books_on_the_current_mouth():
        return json.dumps({'the average count of books that were used for month': round(float_res, 2)})
    return ErrorMessageSchema(message='Статистика отсутствует.').model_dump_json()


def get_top_book() -> json:
    """Получить самую популярную книгу среди студентов, у которых средний балл больше 4.0 (GET)"""
    if book := ReceivingBooksORM.top_book():
        return BookSchema.model_validate(book).model_dump_json()
    return ErrorMessageSchema(message='Статистика отсутствует.').model_dump_json()


def get_top_student() -> json:
    """ Получить ТОП-10 самых читающих студентов в этом году (GET) """
    students = [
        StudentSchema.model_validate(student)
        for student in ReceivingBooksORM.select_top_10_students()
    ]
    if students:
        return CollectionStudentsSchema(students=students).model_dump_json(exclude_none=True)
    return ErrorMessageSchema(message='Статистика отсутствует.').model_dump_json()


def make_file_csv(text_csv: bytes, filename: str) -> None:
    """Создайте роут, который будет принимать csv-файл с данными по студентам (разделитель ;)."""
    csv_content = text_csv.decode('UTF-8')
    with open(file=f'Scripts/{filename}', mode='w', encoding='UTF-8') as file:
        file.write(csv_content)


def make_students_validate_models_from_csv_file(filename: str) -> dict:
    """Создайте роут, который будет принимать csv-файл с данными по студентам (разделитель ;)."""
    models_schema: dict[str, Any] = {}
    students: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    with open(file=f'Scripts/{filename}', mode='r', encoding='UTF-8', newline='') as file:
        reader: csv.DictReader = csv.DictReader(file)

        for row in reader:
            try:
                student = StudentSchema(name=row['name'],
                                        surname=row['surname'],
                                        phone=row['phone'],
                                        email=row['email'],
                                        average_score=row['average_score'],
                                        scholarship=row['scholarship']).model_dump(exclude_none=True)
            except ValidationError as err:
                errors.append(ErrorMessageSchema(message=err).model_dump())
            else:
                students.append(student)

    if errors:
        models_schema['errors'] = errors
    if students:
        models_schema['students'] = students

    return models_schema


def post_models_to_db(list_students: list[dict]) -> None:
    """
        Создайте роут, который будет принимать csv-файл с данными по студентам (разделитель ;).
     Используя csv.DictReader (https://docs.python.org/3/library/csv.html#csv.DictReader),
     обработайте файл и используйте Session.bulk_insert_mappings() для массовой вставки студентов.
     """
    # StudentsORM.insert_collections_students_legacy_feature(students=list_students)
    StudentsORM.insert_collections_students(students=list_students)
