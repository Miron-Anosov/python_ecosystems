import datetime

from typing import Optional

from sqlalchemy import func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from module_21_orm_2.homework.db_orm.models.database_core import BaseModelORM, int_def_1_type
from sqlalchemy.ext.hybrid import hybrid_property

from module_21_orm_2.homework.db_orm.models.database_core import engine


class BooksTable(BaseModelORM):
    """
    -- таблица книг в библиотеке books
    CREATE TABLE IF NOT EXISTS books (
    id integer PRIMARY KEY,
    name text NOT NULL,
    count int default 1,
    release_date date not null,
    author_id int not null)
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'books'  # noqa

    name: Mapped[str]
    count: Mapped[int_def_1_type]
    release_date: Mapped[datetime.datetime]
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))

    authors: Mapped[list['AuthorsTable']] = relationship(back_populates='books')

    students_have_books: Mapped[list['StudentsTable']] = relationship(back_populates='books_list',
                                                                      secondary='receiving_books')


class AuthorsTable(BaseModelORM):
    """
    -- таблица авторов authors
    CREATE TABLE IF NOT EXISTS authors (
    id integer PRIMARY KEY,
    name text NOT NULL,
    surname text NOT NULL
    )
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'authors'  # noqa

    name: Mapped[str]
    surname: Mapped[str]

    books: Mapped[list['BooksTable']] = relationship(back_populates='authors')

    @property
    def count_books(self):
        return sum(book.count for book in self.books)


class StudentsTable(BaseModelORM):
    """
    -- таблица читателей students
    CREATE TABLE IF NOT EXISTS students (
    id integer PRIMARY KEY,
    name text NOT NULL,
    surname text NOT NULL,
    phone text NOT NULL,
    email text NOT NULL,
    average_score float NOT NULL,
    scholarship boolean NOT NULL
    )
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'students'  # noqa

    name: Mapped[str]
    surname: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    average_score: Mapped[float]
    scholarship: Mapped[bool]

    books_list: Mapped[list['BooksTable'] | None] = relationship(back_populates='students_have_books',
                                                                 secondary='receiving_books')


class ReceivingBooksTable(BaseModelORM):
    """
    -- таблица выдачи книг студентам receiving_books
    CREATE TABLE IF NOT EXISTS receiving_books (
    id integer PRIMARY KEY,
    book_id int NOT NULL,
    student_id int NOT NULL,
    date_of_issue datetime not null,
    date_of_return datetime
    )
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'receiving_books'  # noqa

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id', ondelete='CASCADE'))
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'))
    date_of_issue: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    date_of_return: Mapped[Optional[datetime.datetime]]

    @hybrid_property
    def count_date_with_book(self) -> Optional[datetime.datetime]:
        """
         Количество дней, которое читатель держит/держал книгу у себя.
        """
        if self.date_of_return:
            return func.cast(func.julianday(self.date_of_return) - func.julianday(self.date_of_issue), Integer)
        if self.date_of_issue:
            return func.cast(func.julianday(func.now()) - func.julianday(self.date_of_issue), Integer)
        return


def create_all_tables():
    BaseModelORM.metadata.create_all(bind=engine)
