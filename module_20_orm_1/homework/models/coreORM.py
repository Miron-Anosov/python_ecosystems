import datetime
from typing import Optional

from sqlalchemy import select, bindparam, Sequence, insert, and_

from database import get_engine as engine, session_orm
from modelsORM import Books, Students, ReceivingBooks


class WorkerORM:
    session = session_orm(bild=engine(), )


class StudentsORM(WorkerORM):
    _select_stmt_all_students_with_scholarship = (
        select(Students)
        .where(Students.scholarship == 1)
    )

    _select_stmt_avg_scalar_more_scalar_of_input = (
        select(Students)
        .where(Students.average_score > bindparam('average_score'))
    )

    @classmethod
    def select_all_students_with_scholarship(cls) -> Optional[Sequence[Students]]:
        """Получение списка студентов, которые имеют общежитие"""
        with cls.session() as connection:
            return connection.execute(cls._select_stmt_all_students_with_scholarship).scalars().all()

    @classmethod
    def select_avg_scalar_more_scalar_of_input(cls, scalar: int) -> Optional[Sequence[Students]]:
        """
        Получение списка студентов, у которых средний балл выше балла,
        который будет передан входным параметров в функцию
        """
        with cls.session() as connection:
            return connection.execute(cls._select_stmt_avg_scalar_more_scalar_of_input,
                                      {'average_score': scalar, }
                                      ).scalars().all()


class BooksORM(WorkerORM):
    _select_stmt_all_books = select(Books)
    _select_stmt_books_of_late_more_two_weeks = (
        select(ReceivingBooks)
        .where(ReceivingBooks.count_date_with_book > 14)
    )
    _insert_give_books_to_student = (
        insert(ReceivingBooks)
    )

    _select_return_book = (
        select(ReceivingBooks).where(and_
                                     (ReceivingBooks.book_id == bindparam('book_id'),
                                      ReceivingBooks.student_id == bindparam('student_id')))
    )

    @classmethod
    def select_all_books(cls) -> Optional[Sequence[Students]]:
        """
        Получение всех книг в библиотеке
        """
        with cls.session() as connection:
            return connection.execute(cls._select_stmt_all_books).scalars().all()

    @classmethod
    def select_books_of_late_more_two_weeks(cls):
        """Получение список должников, которые держат книги у себя более 14 дней."""
        with cls.session() as connection:
            return connection.execute(cls._select_stmt_books_of_late_more_two_weeks).scalars().all()

    @classmethod
    def insert_give_books_to_student(cls, student_id: int, book_id: int) -> ReceivingBooks:
        """Выдать книгу студенту (POST - входные параметры ID книги и ID студента)"""
        params = {
            'book_id': book_id,
            'student_id': student_id,
            'date_of_issue': datetime.datetime.utcnow(),
        }
        with cls.session() as session:
            receiving_books = ReceivingBooks(**params)
            session.add(receiving_books)
            session.commit()
            return receiving_books

    @classmethod
    def update_return_book(cls, student_id: int, book_id: int):
        """
            Сдать книгу в библиотеку (POST - входные параметры ID книги и ID
            студента, в случае если такой связки нет, выдать ошибку)
        """
        with cls.session() as session:
            return_book = session.execute(cls._select_return_book,
                                          {
                                              'book_id': book_id,
                                              'student_id': student_id,
                                          }
                                          ).scalar()

            return_book.date_of_return = datetime.datetime.utcnow()
            session.commit()
            return return_book

    @classmethod
    def select_book_by_title(cls, title_book: str) -> Books:
        """Будет осуществляться поиск книги по названию."""
        with cls.session() as session:
            return session.query(Books).where(Books.name.contains(title_book)).scalar()
