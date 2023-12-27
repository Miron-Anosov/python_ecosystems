import sqlite3
import sys

from datetime import datetime, timedelta
from typing import Optional, Dict, Set

hobby: Dict[int:str] = {1: 'футбол', 2: 'хоккей', 3: 'шахматы', 4: 'SUP сёрфинг', 5: 'бокс', 6: 'Dota2',
                        7: 'шахбокс', }

update: str = """ UPDATE `table_friendship_schedule` SET `employee_id` = ? WHERE `date` = ? and `employee_id` = ? """
employee_day_off: str = """ SELECT `id` FROM `table_friendship_employees` WHERE `preferable_sport` = ? """
team_of_working_day: str = """ SELECT * FROM `table_friendship_schedule` WHERE `date`  = ?  """


def update_work_schedule(cur: sqlite3.Cursor) -> None:
    """Функция обновляет таблицы сотрудников"""

    days, id_employee = int, int
    data_count_days: Dict[id_employee:days] = {}
    id_workers: Set[id_employee] = set(range(1, 367))
    count_swap_workers: int = 0

    start_date: datetime = datetime(2020, 1, 1)
    end_date: datetime = datetime(2020, 12, 31)
    day_delta: timedelta = timedelta(days=1)
    current_date: datetime = start_date

    def account_working_days(workers_today: Optional[None] | set = None, except_id: set | Optional[None] = None) -> int:
        """Функция составляет анализ рабочих для задействования большей части работников."""
        day: int = 1
        if workers_today:

            for person_id in workers_today:
                if data_count_days.get(person_id):
                    data_count_days[person_id] += day
                else:
                    data_count_days[person_id] = day
        else:

            try:  # Выводим на работу любого, кто еще не в словаре.
                id_worker: int = (id_workers - (set(data_count_days.keys()) | except_id)).pop()
                data_count_days[id_worker] = data_count_days.get(id_worker, 0) + day
                return id_worker

            except (KeyError, ValueError):  # Выводится на работу из словаря, за исключением исключающего списка id
                id_worker: int = next(id_worker for id_worker, _ in sorted(
                    data_count_days.items(), key=lambda item: item[day]) if id_worker not in except_id)
                data_count_days[id_worker] = data_count_days.get(id_worker, 0) + day
                return id_worker

    try:

        while current_date <= end_date:  # Обход всех календарных дней.

            ids_team_current_day: Set[int] = set(worker_id[0] for worker_id in cur.execute(
                team_of_working_day, (current_date.date(),)))
            workers_than_needs_day_off: set[int] = set(worker_id[0] for worker_id in cur.execute(employee_day_off, (
                hobby.get(current_date.isoweekday()),)))
            conflict_date_for_workers: set[id_employee] = ids_team_current_day & workers_than_needs_day_off
            account_working_days(ids_team_current_day - conflict_date_for_workers)

            if conflict_date_for_workers:  # Обновляем БД
                cur.executemany(update, [(account_working_days(except_id=workers_than_needs_day_off),
                                          current_date.date(), id_dya_off)
                                         for id_dya_off in conflict_date_for_workers])
                count_swap_workers += len(conflict_date_for_workers)

            current_date += day_delta  # Обновляем дни.

        else:
            min_days: days = min(data_count_days.values())
            max_days: days = max(data_count_days.values())
            print(f'График обновлен для {count_swap_workers} работников.',
                  f'Минимальное кол-во смен у сотрудников: {min_days}.',
                  f'Максимальное кол-во смен у сотрудников: {max_days}', sep='\n')

    except sqlite3.Error as err:
        print(f"Ошибка при выполнении запроса: {err}", file=sys.stderr)


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
