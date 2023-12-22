import sqlite3


def ivan_sovin_the_most_effective(
        cur: sqlite3.Cursor,
        workers_name: str,
) -> None:
    response: str = """
        SELECT 
            CASE
                WHEN sovin.salary > (worker.salary + (worker.salary * 0.1))
                    THEN 1
                ELSE 0
            END AS "Статус",
            worker.salary + (worker.salary * 0.1) AS new_salary
            
        FROM (SELECT salary FROM `table_effective_manager` WHERE name = "Иван Совин") AS sovin
        JOIN (SELECT salary FROM `table_effective_manager` WHERE name = ? ) AS worker
    """

    salary_increase: str = """ UPDATE `table_effective_manager` SET salary = ? WHERE name = ? """
    retirement: str = """ DELETE FROM `table_effective_manager`  WHERE name = ? """
    try:
        cur.execute(response, (workers_name,))
        result: list[tuple] = cur.fetchall()
        if result:
            decision, salary = bool(result[0][0]), result[0][1]
            if decision:
                cur.execute(salary_increase, (salary, workers_name))
                print(f'Зарплата повышена для {workers_name} на 10 % до {salary}')
            else:
                cur.execute(retirement, (workers_name,))
                print(f"Работник {workers_name} просит завышенную в размере {salary} ставку и был уволен.")
    except sqlite3.Error as err:
        print(f"Ошибка при выполнении запроса: {err}")


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
