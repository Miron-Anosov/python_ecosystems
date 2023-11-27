import os.path
import sqlite3

db = os.path.abspath(os.path.join('hw_3_database.db'))

with sqlite3.connect(database=db) as connect:
    cur = connect.cursor()
    cur.execute("""
                    SELECT
                        COUNT(t1.id)
                    FROM 
                        `table_1` AS t1
                    UNION ALL
                    SELECT
                        COUNT(t2.id)
                    FROM 
                        `table_2` AS t2
                    UNION ALL
                    SELECT
                        COUNT(t3.id)
                    FROM 
                        `table_3` AS t3
     """)
    result = cur.fetchall()
##############################################################
    cur = connect.cursor()
    cur.execute("""
                SELECT
                    COUNT(DISTINCT t1.id)
                FROM 
                    `table_1` AS t1
    """)
    result_2 = cur.fetchall()

    cur = connect.cursor()
    cur.execute("""
                    SELECT
                        COUNT(t2.id)
                    FROM 
                        `table_1` AS t1
                    JOIN 
                        `table_2` AS t2
                    ON 
                        t2.id = t1.id    
    """)
    result_3 = cur.fetchall()
##############################################################
    cur = connect.cursor()
    cur.execute("""
                        SELECT
                            COUNT(t1.id)
                        FROM 
                            `table_1` AS t1
                        JOIN 
                            `table_2` AS t2
                        ON 
                            t2.id = t1.id
                        JOIN
                            `table_3` AS t3
                        ON 
                            t3.id = t1.id 
        """)
    result_4 = cur.fetchall()


#  Сколько записей (строк) хранится в каждой таблице?
for numm, result_table in enumerate(result):
    print(f'Записей в {numm + 1} таблице: {result[numm][0]}')

#  Сколько в таблице table_1 уникальных записей?
print(f'В таблице table_1 уникальных записей: {result_2[0][0]}')

#  Как много записей из таблицы table_1 встречается в table_2?
print(f'Записей из таблицы table_1 встречается в table_2 : {result_3[0][0]}')

#  Как много записей из таблицы table_1 встречается и в table_2, и в table_3?
print(f'Записей из таблицы table_1 встречается и в table_2, и в table_3: {result_4[0][0]}')
