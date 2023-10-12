from datetime import datetime
from typing import Optional


class Manager:
    __storage: dict = {}

    @classmethod
    def add_date(cls, date: str, number: str) -> str:
        result: Optional[bool] = cls.__check_values(date, number)
        if result:
            if cls.__storage.get(date):
                cls.__storage[date] += number
                return f'Datas was update: date:<b>{date}</b> rub:<b>{cls.__storage.get(date)}</b>'
            cls.__storage.setdefault(date, number)
            return f'Created new data: new date:<b>{date}</b> rub:<b>{number}</b>'
        return f"Datas didn't update. Datas aren't correct. ({date=}: {number=}) <br> " \
               f"Format date: <b>YYYY-MM-DD</b><br>" \
               f"Format number <b>integer or float</b>"

    @classmethod
    def __check_values(cls, date_input: str, number: str) -> bool:
        try:
            _: float = float(number)
            datetime.strptime(date_input, '%Y-%m-%d')
            return True
        except TypeError:
            return False

    @classmethod
    def calculate_year_mouth(cls, year: int, mouth: str = None) -> str:
        count_rub = 0
        pattern = f'{year}'
        if mouth:
            pattern = ''.join(f'{pattern}-{mouth:02}')
        for date, rub in cls.__storage.items():
            if pattern in date:
                count_rub += rub
        if count_rub != 0:
            return f'Expenses for <b>{year}</b> year: rub:<b>{count_rub}</b>'
        return f"You didn't have expenses for <b>{year}</b> year"


manager = Manager()
