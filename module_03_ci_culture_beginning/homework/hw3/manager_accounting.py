from datetime import datetime
from typing import Optional


class Manager:
    storage: dict = {}

    def add_date(self, date: str, number: int) -> str:
        """
        Метод применяется для обработки и добавления данных в словарь.
        Args:
            date:str: Дата формата YYYY-MM-DD. Является ключом.
            number:int: Рубли. Является значением ключа date.
        Returns:
            Результат выполнения создания/обновления/ошибки.
        """
        result: Optional[bool] = self.__check_values(date, number)
        if result:
            if self.storage.get(date):
                self.storage[date] += number
                return f'Datas was update: date:<b>{date}</b> rub:<b>{self.storage.get(date)}</b>'
            self.storage.setdefault(date, number)
            return f'Created new data: new date:<b>{date}</b> rub:<b>{number}</b>'
        return f"Datas didn't update. Datas aren't correct. ({date=}: {number=}) <br> " \
               f"Format date: <b>YYYY-MM-DD</b><br>" \
               f"Format number <b>integer or float</b>"

    @classmethod
    def __check_values(cls, date_input: str, number: int) -> bool:
        try:
            _: int = int(number)
            datetime.strptime(date_input, '%Y-%m-%d')
            return True
        except (TypeError, ValueError):
            return False

    def calculate_year_mouth(self, year: int, month: int = None) -> str:
        """
        Метод формирует результат запроса в виде строки с финансовыми результатами за определенный период.

        Args:
            year: int: период запроса в рамках одного года. Используется в качестве ключа.
            month: int: период запроса в рамках одного года в определенный месяц. Используется в качестве ключа.

        Raises:
            None

        Returns:
            Результат запроса результата за год/месяц или сообщение об отсутствии результата.

        """
        count_rub = 0
        pattern = f'{year}'
        if month:
            pattern = ''.join(f'{pattern}-{month:02}')
        for date, rub in self.storage.items():
            if pattern in date:
                count_rub += rub
        if count_rub != 0:
            return f'Expenses for <b>{pattern}</b>: rub:<b>{count_rub}</b>'
        return f"You didn't have expenses for <b>{pattern}</b>"

    def __repr__(self):
        return f'Manager: {self.storage}'


if __name__ == '__main__':
    manager = Manager()
