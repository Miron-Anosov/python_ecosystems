from functools import wraps
from typing import Type

from sqlalchemy.orm import sessionmaker

from .engine import CreatorDB
from .crud import CRUD


class DB:
    def __init__(self, ddl: CreatorDB, dml: Type[CRUD]):
        self.ddl = ddl
        self.dml: CRUD = self.__dml_create(dml)

    def __dml_create(self, dml: Type[CRUD]):
        return dml(session=self.make_session())

    def make_session(self):
        session = sessionmaker(bind=self.ddl.engine, autoflush=False)
        with session() as new_session:
            return new_session

    def with_session(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = self.make_session()
            try:
                result = func(self.dml, *args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        return wrapper


def create_db_worker() -> DB:
    ddl = CreatorDB()
    return DB(ddl=ddl, dml=CRUD)


def create_data():
    db: DB = create_db_worker()
    db.ddl.drop_db()
    db.ddl.create_db()
    db.dml.make_data_to_db_before_request()
    db.ddl.engine.dispose()


db_core = create_db_worker()
