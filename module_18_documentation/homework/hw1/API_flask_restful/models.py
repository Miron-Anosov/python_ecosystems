import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'last_name': 'Swaroop', 'first_name': 'C.', 'middle_name': 'H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'last_name': 'Melville', 'first_name': 'Herman'},
    {'id': 3, 'title': 'War and Peace', 'last_name': 'Tolstoy', 'first_name': 'Leo'},
]
EXIST_OBJECT = 0
TABLES = 2
DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Book:
    title: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None
    author_id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    author_id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}'
            UNION
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchall()
        if len(exists) != TABLES:
            cursor.executescript(
                f"""
                DROP TABLE IF EXISTS`{BOOKS_TABLE_NAME}`;
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author_id INTEGER REFERENCES {AUTHORS_TABLE_NAME}(author_id) ON DELETE CASCADE ON UPDATE CASCADE    
                );

                DROP TABLE IF EXISTS `{AUTHORS_TABLE_NAME}`;
                CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    middle_name VARCHAR(50)
                );
                """
            )
            for item in initial_records:
                cursor.execute(
                    f"""
                    INSERT INTO `{AUTHORS_TABLE_NAME}`
                    (first_name, last_name, middle_name) VALUES (?,?,?);
                    """, (item.get('first_name'), item.get('last_name'), item.get('middle_name'))
                )

                author_id = cursor.lastrowid

                cursor.execute(
                    f"""
                    INSERT INTO `{BOOKS_TABLE_NAME}`
                    (title, author_id) VALUES (?, ?);
                    """, (item['title'], author_id)

                )


def _get_book_obj_from_row(row: tuple) -> Book:
    id_book, author_id, title, first_name, last_name, middle_name = row
    return Book(id=id_book, author_id=author_id, title=title,
                first_name=first_name, last_name=last_name, middle_name=middle_name)


def _get_author_obj_from_row(row: tuple) -> Author:
    author_id, first_name, last_name, middle_name = row
    return Author(first_name=first_name, last_name=last_name, middle_name=middle_name, author_id=author_id)


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
                          SELECT
                             `{BOOKS_TABLE_NAME}`.book_id,
                             `{BOOKS_TABLE_NAME}`.author_id,
                             `{BOOKS_TABLE_NAME}`.title,
                             `{AUTHORS_TABLE_NAME}`.first_name,
                             `{AUTHORS_TABLE_NAME}`.last_name,
                             `{AUTHORS_TABLE_NAME}`.middle_name
                          FROM 
                             `{BOOKS_TABLE_NAME}`
                          JOIN
                             `{AUTHORS_TABLE_NAME}`
                          ON
                             `{BOOKS_TABLE_NAME}`.author_id = `{AUTHORS_TABLE_NAME}`.author_id;""")

        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def get_book_by_id(book_id: int) -> Book:
    with sqlite3.connect(DATABASE_NAME) as coon:
        cursor = coon.cursor()
        cursor.execute(f"""
                        SELECT 
                          `{BOOKS_TABLE_NAME}`.book_id, 
                          `{BOOKS_TABLE_NAME}`.author_id,
                          `{BOOKS_TABLE_NAME}`.title,    
                          `{AUTHORS_TABLE_NAME}`.first_name, 
                          `{AUTHORS_TABLE_NAME}`.last_name, 
                          `{AUTHORS_TABLE_NAME}`.middle_name 
                        FROM 
                           `{BOOKS_TABLE_NAME}` 
                        JOIN 
                           `{AUTHORS_TABLE_NAME}` 
                        ON
                           `{BOOKS_TABLE_NAME}`.author_id = `{AUTHORS_TABLE_NAME}`.author_id 
                        WHERE 
                           `{BOOKS_TABLE_NAME}`.book_id = ?;""", (book_id,))
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_id_author(book: Book) -> int | None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT 
                author_id 
            FROM 
                `{AUTHORS_TABLE_NAME}` 
            WHERE 
                first_name = ? 
            AND 
                last_name = ? 
            AND 
                (middle_name IS NULL OR middle_name = ?);
            """, (book.first_name, book.last_name, book.middle_name))

        author_id = cursor.fetchone()
        if author_id:
            return author_id[EXIST_OBJECT]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        if author_id := get_id_author(book):
            cursor.execute(f"""
                                    INSERT INTO `{BOOKS_TABLE_NAME}`
                                        (title, author_id) 
                                    VALUES (?, ? );""",
                           (book.title, author_id)
                           )

            book.id = cursor.lastrowid
            book.author_id = author_id
            return book

        cursor.execute(
            f"""
                    INSERT INTO `{AUTHORS_TABLE_NAME}`
                        (first_name, last_name, middle_name) 
                    VALUES (?,?,?);""",
            (book.first_name, book.last_name, book.middle_name)
        )

        author_id = cursor.lastrowid
        cursor.execute(f"""
                                INSERT INTO `{BOOKS_TABLE_NAME}`
                                    (title, author_id) 
                                VALUES (?, ?);""",
                       (book.title, author_id)
                       )

        book.id = cursor.lastrowid
        book.author_id = author_id
        return book


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
                    INSERT INTO `{AUTHORS_TABLE_NAME}`
                        (first_name, last_name, middle_name) 
                    VALUES (?,?,?);""",
            (author.first_name, author.last_name, author.middle_name)
        )
        author.author_id = cursor.lastrowid
        return author


def update_book_by_id(book: Book, return_book: Optional[bool] = None) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(f"""
                      UPDATE {BOOKS_TABLE_NAME}
                      SET 
                          title = ?
                      WHERE 
                          book_id = ?;""",
                       (book.title, book.id)
                       )

        cursor.execute(f"""
            UPDATE {AUTHORS_TABLE_NAME}
            SET 
                first_name = ?,
                last_name = ?, 
                middle_name = ?
            WHERE author_id IN (
                SELECT
                    {BOOKS_TABLE_NAME}.author_id
                FROM
                    {BOOKS_TABLE_NAME}
                WHERE
                    {BOOKS_TABLE_NAME}.book_id = ? 
                AND 
                    {BOOKS_TABLE_NAME}.author_id = {AUTHORS_TABLE_NAME}.author_id);
            """, (book.first_name, book.last_name, book.middle_name, book.id))

        conn.commit()
    if return_book:
        return get_book_by_id(book.id)


def get_truth_author_id(author_id: int) -> Optional[bool]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT EXISTS (SELECT 1 FROM `{AUTHORS_TABLE_NAME}`'
                       f'WHERE author_id = ?);', (author_id,))
        author = cursor.fetchone()[EXIST_OBJECT]
        if author:
            return True


def check_author_in_bd(first_name: str, last_name: str, middle_name: str = None):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT EXISTS (
            SELECT 
                1
            FROM 
                `{AUTHORS_TABLE_NAME}` 
            WHERE 
                first_name = ? 
            AND 
                last_name = ? 
            AND 
                (middle_name IS NULL OR middle_name = ?));
            """, (first_name, last_name, middle_name))

        author_exist = cursor.fetchone()[EXIST_OBJECT]
        if author_exist:
            return author_exist


def get_author_by_id(author_id: int) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
                    SELECT 
                        * 
                    FROM 
                        `{AUTHORS_TABLE_NAME}`
                    WHERE 
                        author_id = ?;""", (author_id,))
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_truth_book_id(book_id: int) -> Optional[bool]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT EXISTS (SELECT 1 FROM `{BOOKS_TABLE_NAME}`'
                       f'WHERE book_id = ?);', (book_id,))
        book = cursor.fetchone()[EXIST_OBJECT]
        if book:
            return True


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE book_id = ?
            """,
            (book_id,)
        )
        conn.commit()


def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute(
            f"""
            DELETE 
            FROM 
                {AUTHORS_TABLE_NAME}
            WHERE 
                author_id = ?
            """,
            (author_id,)
        )
        conn.commit()


def check_book(title: str) -> Optional[bool]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
                        SELECT EXISTS(
                        SELECT 
                             1
                        FROM
                           `{BOOKS_TABLE_NAME}`
                        JOIN
                           `{AUTHORS_TABLE_NAME}`
                        ON
                           `{BOOKS_TABLE_NAME}`.author_id = `{AUTHORS_TABLE_NAME}`.author_id
                        WHERE 
                           `{BOOKS_TABLE_NAME}`.title = ?

                           );""",
                       (title,))

        book = cursor.fetchone()[EXIST_OBJECT]
        if book:
            return True