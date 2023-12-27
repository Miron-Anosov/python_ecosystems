import random
import sqlite3

from module_13_db2.homework.hw5.constants import countries, teams, level


def _get_country() -> str:
    random_country: str = random.choice(countries)
    countries.remove(random_country)
    return random_country


def _get_name_command() -> str:
    random_name: str = random.choice(teams)
    teams.remove(random_name)
    return random_name


def _get_force(level_command: int) -> str:
    index: int = level_command % len(level)
    return level[index]


def generate_test_data(cur: sqlite3.Cursor, number_of_groups_: int) -> None:
    try:

        cur.executemany((
            """
            INSERT INTO `uefa_commands` (command_number, command_name, command_country, command_level)
            VALUES (?, ?, ?, ?) """),
            [(numbs_command, _get_name_command(), _get_country(), _get_force(numbs_command))
             for numbs_command in range(1, number_of_groups_ * 4 + 1)])

        cur.executemany(("""
                INSERT INTO `uefa_draw` (command_number, group_number) VALUES (?, ?) """),
                        [(numbs_command + 1, (numbs_command // 4) + 1)
                         for numbs_command in range(number_of_groups_ * 4)])

    except sqlite3.Error as err:
        print(f"Ошибка при выполнении запроса: {err}")


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
