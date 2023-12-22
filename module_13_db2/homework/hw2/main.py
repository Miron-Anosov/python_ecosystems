import csv
import sqlite3
import logging

logger = logging.getLogger(__name__)


def delete_wrong_fees(cur: sqlite3.Cursor, wrong_fees_file: str) -> None:

    sql_request: str = """
    DELETE
    FROM 
        `table_fees`
    WHERE `truck_number` = ? AND `timestamp` = ?
    """
    try:

        with open(file=wrong_fees_file, encoding="windows-1251", mode='r') as csv_file:
            reader = csv.reader(csv_file)
            _ = next(reader)

            for count, wrong_fine in enumerate(reader, 1):
                car_number, date = wrong_fine
                logger.warning(f'№{count}: DELETED {car_number}, data: {date}')
                cur.execute(sql_request, (car_number, date))

    except IOError as err:
        logger.error(err)


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
