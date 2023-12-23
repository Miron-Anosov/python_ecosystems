import sqlite3
import logging
from sqlite3 import Connection, Cursor, Error, OperationalError
from typing import Optional, List

logger: logging = logging.getLogger(__name__)

__all__ = ['sqlite_manager']


class SqLite3DBConnect:
    """
    Класс описывает минимальный набор для работы с базой данных о «Звёздных войнах»
    """

    def __init__(self, name_db: str, name_table: str) -> None:
        """
        Конструктор создает или подключается у уже имеющейся БД.
        Args:
            name_db: Название бд.
            name_table: Название талицы.
        """
        self.__name_db: str = f'{name_db}.db'
        self.__name_table: str = name_table
        self.__connect: Optional[None] | Connection = None

    def __enter__(self):
        if not self.__connect:
            try:
                logger.debug(f'Connect at {self.__name_db}')
                self.__connect: Connection = sqlite3.connect(self.__name_db)
                self.__connect.row_factory = sqlite3.Row
                self._check_bd()
                self.__connect.commit()
            except Error as e:
                self.__connect.close()
                logger.error(e)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type:
                logger.error(exc_type)
        finally:
            self.__connect.close()

    def _check_bd(self) -> None:
        """
        Метод создает таблицу в БД, в случае ее отсутствия.
        Returns:
            None
        """
        with self.__connect as con:
            cur: Cursor = con.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.__name_table} ("
                        f"actor_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                        f"name TEXT NOT NULL,"
                        f"age TEXT NOT NULL,"
                        f"gender TEXT NOT NULL"
                        f");")
        logger.debug(f'Check table: {self.__name_table}')

    def insert_new_actor(self, name: str, age: str, gender: str, name_table: str = 'person') -> None:
        """
        Метод добавляет новые списки в таблицу.
        Args:
            name: str:  Имя персонажа.
            age: int: Возраст персонажа.
            gender: str:  Гендер персонажа.
            name_table: Название таблицы.

        Returns:
            None
        """
        try:
            with self.__connect as con:
                cur: Cursor = con.cursor()
                cur.execute(f"INSERT INTO {name_table} (name, age, gender) VALUES (?, ?, ?);", (name, age, gender))
                logger.debug(f'Insert a new person: {name, age, gender} in table: {name_table}')
        except OperationalError:
            logger.error('sqlite3.OperationalError: database is locked. Insert fail')

    def select(self, *args, name_table: str = 'person') -> List[sqlite3.Row]:
        """
        Метод возвращает данные из таблицы.
        Args:
            *args: Поля.
            name_table: Название таблицы

        Returns:
            List[sqlite3.Row]
        """
        columns: str = '*'
        if args:
            columns = ','.join(args)
        with self.__connect as con:
            cur: Cursor = con.cursor()
            cur.execute(f"SELECT {columns}  FROM {name_table};")
            result: List[sqlite3.Row] = cur.fetchall()
            logger.debug(f'Select {columns} from {name_table}')
            return result

    def drop(self, name_table: str) -> None:
        """
        Удаление данных из таблицы.
        Args:
            name_table: Имя таблицы

        Returns:
            None
        """
        try:
            with self.__connect as con:
                con.execute(f"DROP TABLE IF EXISTS {name_table}")
                logger.debug(f'Table is dropped')
        except OperationalError:
            logger.error(f"sqlite3.OperationalError: database is locked. DB didn't dropped")


def sqlite_manager(name_db: str = 'actors_from_sw', name_table: str = 'person') -> SqLite3DBConnect:
    """
    Функция возвращает объект СУБД sqlite3
    Args:
        name_db:Название бд.
        name_table: Имя таблицы.

    Returns:
        SqLite3DBConnect
    """
    base: SqLite3DBConnect = SqLite3DBConnect(name_db=name_db, name_table=name_table)
    return base
