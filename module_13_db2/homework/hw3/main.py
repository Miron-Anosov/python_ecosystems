import datetime
import sqlite3

drop_table: str = """
DROP TABLE IF EXISTS `table_birds`;
"""

create_table: str = """
CREATE TABLE IF NOT EXISTS `table_birds`(
    id INTEGER PRIMARY KEY,
    type_bird VARCHAR(255) NOT NULL,
    meeting VARCHAR(255) NOT NULL,
    amount INTEGER NOT NULL
);"""


def log_bird(
        cur: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
        amount: int
) -> None:
    insert: str = """
    INSERT INTO `table_birds` (type_bird, meeting, amount) VALUES (?,?,?)
    """
    try:
        cur.execute(insert, (bird_name, date_time, amount))

        print("Новая птица теперь в БД")

    except sqlite3.Error as err:
        print(f"Ошибка при выполнении запроса: {err}")


def check_if_such_bird_already_seen(
        cur: sqlite3.Cursor,
        bird_name: str
) -> bool:
    check_bird: str = """
                        SELECT  EXISTS (SELECT 1 FROM `table_birds` WHERE  type_bird = (?) )
                      """
    try:
        cur.execute(check_bird, (bird_name,))
        result_bool: bool = bool(cur.fetchone()[0])

        return result_bool

    except sqlite3.Error as err:
        print(f"Ошибка при выполнении запроса: {err}")


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ").strip().capitalize()
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        # cursor.execute(drop_table)
        cursor.execute(create_table)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
        else:
            log_bird(cursor, name, right_now, count)
