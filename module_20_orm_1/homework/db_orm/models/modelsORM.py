import datetime

from typing import Optional

from sqlalchemy import func, Integer
from sqlalchemy.orm import Mapped
from module_20_orm_1.homework.db_orm.models.database_core import BaseModelORM, int_def_1_type
from sqlalchemy.ext.hybrid import hybrid_property


class Books(BaseModelORM):
    """
    -- таблица книг в библиотеке books
    CREATE TABLE IF NOT EXISTS books (
    id integer PRIMARY KEY,
    name text NOT NULL,
    count int default 1,
    release_date date not null,
    author_id int not null)
    """
    name: Mapped[str]
    count: Mapped[int_def_1_type]
    release_date: Mapped[datetime.datetime]
    author_id: Mapped[int]


class Authors(BaseModelORM):
    """
    -- таблица авторов authors
    CREATE TABLE IF NOT EXISTS authors (
    id integer PRIMARY KEY,
    name text NOT NULL,
    surname text NOT NULL
    )
    """
    name: Mapped[str]
    surname: Mapped[str]


class Students(BaseModelORM):
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
    name: Mapped[str]
    surname: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    average_score: Mapped[float]
    scholarship: Mapped[bool]


class ReceivingBooks(BaseModelORM):
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
    __tablename__ = 'receiving_books'
    book_id: Mapped[int]
    student_id: Mapped[int]
    date_of_issue: Mapped[datetime.datetime]
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
