import sqlite3

with sqlite3.connect('hw_4_database.db') as conn:
    cur = conn.cursor()
    # Выяснить, сколько человек с острова N находятся за чертой бедности, то есть получает меньше 5000 гульденов в год.
    cur.execute("""
                SELECT 
                    COUNT(salary)
                FROM 
                    salaries
                WHERE 
                    salaries.salary < 5000;
    """)
    poor = cur.fetchall()[0][0]

    # Посчитать среднюю зарплату по острову N.
    cur.execute("""
                SELECT
                    ROUND(AVG(salary))
                FROM 
                    salaries;
    """)

    avg = cur.fetchall()[0][0]

    # Посчитать медианную зарплату по острову.
    cur.execute("""
                    SELECT
                        salary
                    FROM 
                        salaries
                    ORDER BY 
                        salary
                    LIMIT 1  OFFSET (SELECT
                                        COUNT(salary)
                                    FROM salaries
                                     ) / 2;
                    
        """)

    mid = cur.fetchall()[0][0]

    # Посчитать число социального неравенства F
    cur.execute("""
                SELECT
                    ROUND((SUM(rich.salary)* 100.0) / (SELECT SUM(salary) - SUM(rich.salary) FROM salaries),2)
                AS `F = T/K`           
                FROM (SELECT * FROM  salaries 
                      ORDER BY salary 
                      LIMIT CAST((SELECT COUNT(id) * 0.1 FROM salaries) 
                      AS INTEGER))
                AS rich 
                """)

    rich = cur.fetchall()[0][0]

print(f'Получает меньше 5000 гульденов в год: {poor:,}')
print(f'Посчитать среднюю зарплату по острову N: {avg:,}')
print(f'Посчитать медианную зарплату по острову: {mid:,}')
print(f'Посчитать число социального неравенства F: {rich}')
