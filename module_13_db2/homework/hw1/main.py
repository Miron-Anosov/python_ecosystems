import sqlite3


def check_if_vaccine_has_spoiled(cur: sqlite3.Cursor, truck_number_str: str) -> bool:
    request_sql: str = """
                    SELECT
                            EXISTS (
                                    SELECT 
                                        1
                                    FROM 
                                        `table_truck_with_vaccine`
                                    WHERE 
                                        `truck_number` = ? 
                                        AND (`temperature_in_celsius` BETWEEN 16 AND 20) = 0
                            )
                """
    cur.execute(request_sql, (truck_number_str,))
    condition: bool = bool(cur.fetchone()[0])
    return condition


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
