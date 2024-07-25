# В модуле реализован класс для работы с таблицами БД.

from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import select, insert, Sequence, Row, RowMapping, func
from sqlalchemy.dialects.postgresql import to_tsvector

from .orm.user import UserORM
from .orm.coffee import CoffeeORM
from ..services.make_valid_data import make_data_for_db


class CRUD:
    def __init__(self, session: Session) -> None:
        self.session = session

    def insert_client(self, user_data: list[dict]) -> UserORM:
        """Создается новый пользователь."""
        return self.session.scalars(insert(UserORM).returning(UserORM), user_data).one()

    def select_coffee_by_name(self, type_coffee: str) -> Sequence[CoffeeORM]:
        """Поиск кофе по названию с применением полнотекстового поиска."""
        return self.session.execute(select(CoffeeORM).where(
            to_tsvector(CoffeeORM.title).match(type_coffee))).scalars().all()

    def select_unique_ingredients(self) -> Sequence[Row | RowMapping | Any]:
        """Список уникальных элементов в заметках к кофе."""
        return self.session.execute(
            select(func.unnest(CoffeeORM.notes)).order_by(func.unnest(CoffeeORM.notes)).distinct()).scalars().all()

    def select_clients_by_country(self, country: str, json_key: str = 'country') -> Sequence[UserORM]:
        """Список пользователей, проживающих в стране (страна — входной параметр)."""
        return self.session.execute(select(UserORM).where(
            func.json_extract_path_text(UserORM.address, json_key) == country)).scalars().all()

    def make_data_to_db_before_request(self) -> None:
        """
        Создает объекты Coffee и User в базе данных.

        Notes:
            make_data_for_db() возвращает tuple:
               - coffee: list[dict]: Данные для создания объекта Coffee.
               - users: list[dict]: Данные для создания объекта User.
        """
        coffee, users = make_data_for_db()
        with self.session.begin():
            for create_coffee, create_user in zip(coffee, users):
                new_coffee = CoffeeORM(**create_coffee)
                self.session.add(new_coffee)
                self.session.flush()
                create_user["coffee_id"] = new_coffee.id
                user = UserORM(**create_user)
                self.session.add(user)
