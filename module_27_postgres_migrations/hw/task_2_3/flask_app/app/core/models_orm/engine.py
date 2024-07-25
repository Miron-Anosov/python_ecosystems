from sqlalchemy import create_engine, Engine

from ..settings import settings
from .orm.basemodel import BaseModel


class CreatorDB:
    """Клас отвечает за инициализацию ORM движка и создание таблиц."""

    def __init__(self):
        self.engine: Engine = self.__get_engine()

    def create_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)

    @staticmethod
    def __get_engine() -> Engine:
        connection_url: str = settings.connection_url_to_db
        return create_engine(connection_url, echo=True)
