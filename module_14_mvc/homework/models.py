import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]

UPDATE_VIEW_AUTHOR = """UPDATE `table_books` SET number_of_views = number_of_views + 1 WHERE `author` = ?"""
UPDATE_VIEW_ALL = """UPDATE `table_books` SET number_of_views = number_of_views + 1"""
INSERT_NEW_BOOK = """INSERT INTO 'table_books'(title, author) VALUES(?, ?)"""
SELECT_AUTHOR = """SELECT `id`, `title`, `author` FROM `table_books` WHERE `author` = ?"""


class Book:

    def __init__(self, id_: int, title: str = None, author: str = None, count_use: int = 0) -> None:
        self.id: int = id_
        self.title: str = title
        self.author: str = author
        self.count: int = count_use

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE IF NOT EXISTS `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    number_of_views INTEGER DEFAULT 0
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )


def get_all_books(page_books_id: bool = False) -> List[Book]:
    id_index: int = 0
    count_view: int = 1
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        _update_count_view(cursor=cursor)
        conn.commit()
        if page_books_id:
            cursor.execute(
                """
                SELECT `id`, `number_of_views` from `table_books`
                """
            )
            books: List[Book] = [Book(id_=row[id_index], count_use=row[count_view]) for row in cursor.fetchall()]
            return books
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        return [Book(*row) for row in cursor.fetchall()]


def add_book_in_table(title: str, author: str) -> None:
    """Добавление новой книги в БД."""
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(INSERT_NEW_BOOK, (title, author))
        conn.commit()


def search_author(author: str) -> List[Book]:
    """Поиск книг по автору."""
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(SELECT_AUTHOR, (author,))
        books: List[Book] = [Book(*row) for row in cursor.fetchall()]
        _update_count_view(cursor=cursor, author=author)
        conn.commit()
        return books


def _update_count_view(cursor: sqlite3.Cursor, author: str = None) -> None:
    """Обновляем кол-во просмотров книг."""
    if author:
        cursor.execute(UPDATE_VIEW_AUTHOR, (author,))
    else:
        cursor.execute(UPDATE_VIEW_ALL)
