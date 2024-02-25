import datetime

from typing import Optional, Iterable

from sqlalchemy import select, bindparam, Sequence, insert, and_

from module_20_orm_1.homework.db_orm.models.database_core import session_orm
from module_20_orm_1.homework.db_orm.models.modelsORM import Books, Students, ReceivingBooks


class WorkerORM:
    Session = session_orm()


class StudentsORM(WorkerORM):
    _select_stmt_students_of_late_more_two_weeks = (
        select(Students)
        .join(ReceivingBooks, ReceivingBooks.student_id == Students.id)
        .where(ReceivingBooks.count_date_with_book > 14)
    )

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

        with cls.Session() as connection:
            return connection.execute(cls._select_stmt_all_students_with_scholarship).scalars().all()

    @classmethod
    def select_avg_scalar_more_scalar_of_input(cls, scalar: int) -> Optional[Sequence[Students]]:
        """
        Получение списка студентов, у которых средний балл выше балла,
        который будет передан входным параметров в функцию
        """

        with cls.Session() as connection:
            return connection.execute(cls._select_stmt_avg_scalar_more_scalar_of_input,
                                      {'average_score': scalar, }
                                      ).scalars().all()

    @classmethod
    def select_students_who_late_more_two_weeks(cls) -> Optional[Iterable[Students]]:
        """Получение список должников, которые держат книги у себя более 14 дней."""

        with cls.Session() as connection:
            return connection.execute(cls._select_stmt_students_of_late_more_two_weeks).scalars().all()


class BooksORM(WorkerORM):

    _select_stmt_all_books = select(Books)

    @classmethod
    def select_all_books(cls) -> Optional[Iterable[Books]]:
        """ Получение всех книг в библиотеке. """

        with cls.Session() as connection:
            return connection.execute(cls._select_stmt_all_books).scalars().all()

    @classmethod
    def select_book_by_title(cls, title_book: str) -> Books:
        """Будет осуществляться поиск книги по названию."""

        with cls.Session() as session:
            return session.query(Books).where(Books.name.contains(title_book)).scalar()


class ReceivingBooksORM(WorkerORM):
    _select_stmt_return_book_order = (
        select(ReceivingBooks).where(and_
                                     (ReceivingBooks.book_id == bindparam('book_id'),
                                      ReceivingBooks.student_id == bindparam('student_id')))
    )

    _insert_stmt_receiving_book = (
        insert(ReceivingBooks).values(book_id=bindparam('book_id'),
                                      student_id=bindparam('student_id'),
                                      date_of_issue=bindparam('date_of_issue'),
                                      )
    )

    @classmethod
    def insert_give_books_to_student(cls, student_id: int, book_id: int) -> ReceivingBooks | None:
        """Выдать книгу студенту (POST - входные параметры ID книги и ID студента)"""

        with cls.Session() as session:
            receiving_book = ReceivingBooks(book_id=book_id,
                                            student_id=student_id,
                                            date_of_issue=datetime.datetime.utcnow(),)
            session.add(receiving_book)
            session.commit()
            return session.get(ReceivingBooks, receiving_book.id)

    @classmethod
    def update_return_book(cls, student_id: int, book_id: int) -> ReceivingBooks | None:
        """
            Сдать книгу в библиотеку (POST - входные параметры ID книги и ID
            студента, в случае если такой связки нет, выдать ошибку)
        """

        with cls.Session() as session:  # todo переделать под простой insert
            return_book_order = session.execute(cls._select_stmt_return_book_order,
                                                {
                                                    'book_id': book_id,
                                                    'student_id': student_id,
                                                }
                                                ).scalar()
            if return_book_order is None:
                return
            return_book_order.date_of_return = datetime.datetime.utcnow()
            session.commit()

            return_book_order = session.execute(cls._select_stmt_return_book_order,
                                                {
                                                    'book_id': book_id,
                                                    'student_id': student_id,
                                                }
                                                ).scalar()
            return return_book_order
