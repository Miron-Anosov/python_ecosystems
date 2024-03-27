import datetime

from typing import Optional, Iterable

from sqlalchemy import select, bindparam, Sequence, insert, and_, func, desc
from sqlalchemy.orm import selectinload

from module_21_orm_2.homework.db_orm.models.modelsORM import (BooksTable, StudentsTable, ReceivingBooksTable,
                                                              AuthorsTable)
from module_21_orm_2.homework.db_orm.models.database_core import session_orm


class WorkerORM:
    Session = session_orm()


class StudentsORM(WorkerORM):
    _select_stmt_students_of_late_more_two_weeks = (
        select(StudentsTable)
        .join(ReceivingBooksTable, ReceivingBooksTable.student_id == StudentsTable.id)
        .where(ReceivingBooksTable.count_date_with_book > 14)
    )

    _select_stmt_all_students_with_scholarship = (
        select(StudentsTable)
        .where(StudentsTable.scholarship == 1)
    )

    _select_stmt_avg_scalar_more_scalar_of_input = (
        select(StudentsTable)
        .where(StudentsTable.average_score > bindparam('average_score'))
    )

    @classmethod
    def select_all_students_with_scholarship(cls) -> Optional[Sequence[StudentsTable]]:
        """Получение списка студентов, которые имеют общежитие"""

        with cls.Session() as connection:
            return connection.execute(cls._select_stmt_all_students_with_scholarship).scalars().all()

    @classmethod
    def select_avg_scalar_more_scalar_of_input(cls, scalar: int) -> Optional[Sequence[StudentsTable]]:
        """
        Получение списка студентов, у которых средний балл выше балла,
        который будет передан входным параметров в функцию
        """

        with cls.Session() as connection:
            return connection.execute(cls._select_stmt_avg_scalar_more_scalar_of_input,
                                      {'average_score': scalar, }
                                      ).scalars().all()

    @classmethod
    def select_students_who_late_more_two_weeks(cls) -> Optional[Iterable[StudentsTable]]:
        """Получение список должников, которые держат книги у себя более 14 дней."""

        with cls.Session() as connection:
            return connection.execute(cls._select_stmt_students_of_late_more_two_weeks).scalars().all()

    @classmethod
    def select_book_by_authors_that_is_not_read(cls, id_student) -> Optional[Iterable[BooksTable]]:
        """
        Получить список книг, которые студент не читал, при этом другие книги этого автора студент уже брал
        (GET - входной параметр - ID студента).
        Пример: Я брал книгу Льва Толстого “Война и мир”, роут должен вернуть другие.
        """
        with cls.Session() as connection:
            sub = (select(ReceivingBooksTable.book_id).where(
                ReceivingBooksTable.student_id == bindparam('student_id'))).subquery()

            result = connection.execute(
                select(BooksTable).where(BooksTable.id.notin_(sub.select())),
                params={'student_id': id_student}).scalars().all()

            return result

    @classmethod
    def insert_collections_students_legacy_feature(cls, students: list[dict]):
        """
            Создайте роут, который будет принимать csv-файл с данными по студентам (разделитель ;).
         Используя csv.DictReader (https://docs.python.org/3/library/csv.html#csv.DictReader),
         обработайте файл и используйте Session.bulk_insert_mappings() для массовой вставки студентов.

         This method is a legacy feature as of the 2.0 series of SQLAlchemy.
         For modern bulk INSERT and UPDATE, see the sections ORM Bulk INSERT Statements and
         ORM Bulk UPDATE by Primary Key.
         The 2.0 API shares implementation details with this method and adds new features as well.
         https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings
         """
        with cls.Session() as session:
            session.bulk_insert_mappings(StudentsTable, students, return_defaults=True)
            session.commit()

    @classmethod
    def insert_collections_students(cls, students: list[dict]):
        """
            Создайте роут, который будет принимать csv-файл с данными по студентам (разделитель ;).
         Используя csv.DictReader (https://docs.python.org/3/library/csv.html#csv.DictReader),
         обработайте файл и используйте Session.bulk_insert_mappings() для массовой вставки студентов.
        """
        with cls.Session() as session:
            session.execute(insert(StudentsTable), students)
            session.commit()


class BooksORM(WorkerORM):
    _select_stmt_all_books = select(BooksTable)
    _select_stmt_books_by_authors = select(AuthorsTable).options(selectinload(AuthorsTable.books))

    @classmethod
    def select_all_books(cls) -> Optional[Iterable[BooksTable]]:
        """ Получение всех книг в библиотеке. """
        with cls.Session() as connection:
            return connection.execute(cls._select_stmt_all_books).scalars().all()

    @classmethod
    def select_book_by_title(cls, title_book: str) -> BooksTable:
        """Будет осуществляться поиск книги по названию."""

        with cls.Session() as session:
            return session.query(BooksTable).where(BooksTable.name.contains(title_book)).scalar()

    @classmethod
    def select_count_books_by_authors(cls) -> Optional[Iterable[AuthorsTable]]:
        """
        Получить кол-во оставшихся в библиотеке книг по автору (GET -входной параметр - ID автора)
        """

        with cls.Session() as session:
            return session.execute(cls._select_stmt_books_by_authors).scalars().all()


class ReceivingBooksORM(WorkerORM):
    ONE_COPY_OF_THE_BOOK: int = 1

    _select_stmt_return_book_order = (
        select(ReceivingBooksTable).where(and_(
            ReceivingBooksTable.book_id == bindparam('book_id'),
            ReceivingBooksTable.student_id == bindparam('student_id')))
    )

    _insert_stmt_receiving_book = (
        insert(ReceivingBooksTable).values(book_id=bindparam('book_id'),
                                           student_id=bindparam('student_id'),
                                           date_of_issue=bindparam('date_of_issue'),
                                           )
    )

    @classmethod
    def insert_give_books_to_student(cls, student_id: int, book_id: int) -> ReceivingBooksTable | None:
        """Выдать книгу студенту (POST - входные параметры ID книги и ID студента)"""

        with cls.Session() as session:
            receiving_book = ReceivingBooksTable(book_id=book_id,
                                                 student_id=student_id,
                                                 date_of_issue=datetime.datetime.utcnow(), )
            book = session.get(BooksTable, book_id)

            book.count -= cls.ONE_COPY_OF_THE_BOOK
            # В модуле 21 не забывайте обновлять поле Book.count когда берут или возвращают книги.

            session.add(receiving_book)
            session.commit()
            return session.get(ReceivingBooksTable, receiving_book.id)

    @classmethod
    def update_return_book(cls, student_id: int, book_id: int) -> ReceivingBooksTable | None:
        """
            Сдать книгу в библиотеку (POST - входные параметры ID книги и ID
            студента, в случае если такой связки нет, выдать ошибку)
        """

        with cls.Session() as session:
            return_book_order = session.execute(cls._select_stmt_return_book_order,
                                                {
                                                    'book_id': book_id,
                                                    'student_id': student_id,
                                                }
                                                ).scalar()
            if return_book_order is None:
                return

            book = session.get(BooksTable, book_id)
            book.count += cls.ONE_COPY_OF_THE_BOOK
            # В модуле 21 не забывайте обновлять поле Book.count когда берут или возвращают книги.

            return_book_order.date_of_return = datetime.datetime.utcnow()
            session.commit()

            return_book_order = session.execute(cls._select_stmt_return_book_order,
                                                {
                                                    'book_id': book_id,
                                                    'student_id': student_id,
                                                }
                                                ).scalar()
            return return_book_order

    @classmethod
    def select_avg_books_on_the_current_mouth(cls) -> float | None:
        """
            Получить среднее кол-во книг, которые студенты брали в этом месяце (GET)

            WITH table_st AS (
            SELECT
            COUNT(*) as avg_books
            FROM receiving_books
            WHERE (receiving_books.date_of_issue BETWEEN DATE('now', '-31 days') AND DATE('now'))
            GROUP BY student_id )
            SELECT AVG(avg_books) FROM table_st
        """
        with (cls.Session() as connect):
            cte = (select(func.count(ReceivingBooksTable.book_id).label('avg_books'))
                   .where(ReceivingBooksTable.date_of_issue
                          .between(func.DATE('now', '-31 days'), func.DATE('now')))
                   .group_by(ReceivingBooksTable.student_id)
                   ).cte('table_st').select()

            return connect.execute(func.AVG(cte.c.avg_books)).scalar()

    @classmethod
    def top_book(cls) -> Optional[BooksTable]:
        """
            Получить самую популярную книгу среди студентов, у которых средний балл больше 4.0 (GET)

            SELECT COUNT(book_id) as top FROM receiving_books
            WHERE (SELECT students.average_score FROM students)> 4
            GROUP BY book_id
            ORDER BY top DESC
            LIMIT 1
         """
        with cls.Session() as conn:
            top_students_cte = (select(StudentsTable.average_score)).scalar_subquery()
            id_book_stmt = (
                select(func.count(ReceivingBooksTable.book_id).label('top'))
                .where(top_students_cte > 4)
                .group_by(ReceivingBooksTable.book_id)
                .order_by(desc('top'))
                .limit(1)
            )
            id_top_book = conn.execute(id_book_stmt).scalar()
            return conn.get(BooksTable, id_top_book)

    @classmethod
    def select_top_10_students(cls) -> Optional[Iterable[StudentsTable]]:
        """
            Получить ТОП-10 самых читающих студентов в этом году (GET)

            SELECT
                students.id,
                students.name,
                students.surname,
                students.phone,
                students.email,
                students.average_score,
                students.scholarship
            FROM students
            JOIN receiving_books ON receiving_books.student_id = students.id
            WHERE receiving_books.date_of_issue BETWEEN DATE('now', '-356 days') AND DATE('now')
            GROUP BY receiving_books.student_id
            ORDER BY count(receiving_books.id) DESC
            LIMIT 10
        """
        with cls.Session() as session:
            return session.execute(
                select(StudentsTable)
                .join(ReceivingBooksTable)
                .where(ReceivingBooksTable.date_of_issue
                       .between(func.DATE('now', '-365 days'), func.DATE('now')))
                .group_by(ReceivingBooksTable.student_id)
                .order_by(func.count(ReceivingBooksTable.id).desc())
                .limit(10)
            ).scalars().all()


if __name__ == '__main__':
    BooksORM.select_count_books_by_authors()
