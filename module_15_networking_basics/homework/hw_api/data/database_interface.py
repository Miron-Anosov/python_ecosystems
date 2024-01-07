import sqlite3

from typing import TypeVar, Dict, Optional

from module_15_networking_basics.homework.hw_api.data.models.constants_requests_db import *
from module_15_networking_basics.homework.hw_api.data.models.room_model import Room

T = TypeVar('T')


class DBConnect:
    """Класс проверяет наличие бд, в случае отсутствия, генерирует."""
    def __init__(self) -> None:
        self.__check_db()

    @staticmethod
    def __check_db():
        with sqlite3.connect(database=DB_PATH, check_same_thread=False) as connect:
            cursor = connect.cursor()
            try:
                cursor.execute(SELECT_BASE)
            except sqlite3.OperationalError:
                cursor.executescript(CREATE_DB)


class DBWorker(DBConnect):
    """
    Класс выполняет запросы к базе данных через родительский класс DBConnect
    """

    def __init__(self, model_room: T) -> None:
        super().__init__()
        self.model_room: T = model_room

    @staticmethod
    def create_room(new_room: Dict[str, int]) -> None:
        """
        Метод добавляет новые комнаты в БД.
        :param new_room: Dict: {"floor": int, "beds": int, "guestNum": int, "price": int}
        :return: None
        """
        data_for_inset_room = tuple(item for item in new_room.values())
        with sqlite3.connect(database=DB_PATH, check_same_thread=False) as connect:
            cursor = connect.cursor()
            cursor.execute(INSERT_ROOM, data_for_inset_room)
            connect.commit()

    def get_rooms(self) -> Dict[str, list]:
        """
        Метод возвращает список номеров.
        :return: Dict: dict{"roomId": int, "floor": int, "beds": int, "guestNum": int, "price": int}
        """
        with sqlite3.connect(database=DB_PATH, check_same_thread=False) as connect:
            cursor = connect.cursor()
            cursor.execute(SELECT_ALL_FREE_ROOMS)
            return {"rooms": [self.model_room(*row).return_data() for row in cursor.fetchall()]}

    @staticmethod
    def booking(person: Dict) -> Optional[bool]:
        """
        Метод добавляет в таблицу booking бронь и возвращает результат успешности выполненного бронирования.
        :param person: Dict : {'bookingDates': {'checkIn': 20210308, 'checkOut': 20210311},
                                    'firstName': 'John', 'lastName': 'Smith', 'roomId': 11}
        :return: bool
        """
        booking_data = person['bookingDates']
        guest_data = person['firstName'], person['lastName'], person['roomId']

        checkin, checkout = booking_data['checkIn'], booking_data['checkOut']
        firstname, lastname, id_room = guest_data

        with sqlite3.connect(database=DB_PATH, check_same_thread=False) as connect:
            cursor = connect.cursor()
            cursor.execute(SELECT_BOOKING, (id_room,))
            if not cursor.fetchone():
                cursor.execute(INSET_GUEST, (id_room, firstname, lastname, checkout, checkin))
                connect.commit()
                return True
            return False


def db_worker():
    """Функция передает объект интерфейса работы с бд."""
    return DBWorker(model_room=Room)
