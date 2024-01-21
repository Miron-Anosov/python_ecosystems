import sqlite3

from requests_const import requests_sql_data

with sqlite3.connect('hw.db') as connect:
    cursor = connect.cursor()
    for request in requests_sql_data:
        cursor.executescript(request)
