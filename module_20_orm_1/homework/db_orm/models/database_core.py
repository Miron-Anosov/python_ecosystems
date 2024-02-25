from typing import Annotated
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, declared_attr, Mapped, Session, sessionmaker

url_sqlite_def = 'sqlite+pysqlite:///library.db'

int_pr_key_type = Annotated[int, mapped_column(primary_key=True)]
int_def_1_type = Annotated[int, mapped_column(default=1)]


def get_engine(url: str = url_sqlite_def) -> Engine:
    return create_engine(url=url, echo=True)


_engine = get_engine()


def session_orm(bild=_engine) -> sessionmaker[Session]:
    return sessionmaker(bind=bild)


class BaseModelORM(DeclarativeBase):
    id: Mapped[int_pr_key_type]

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __repr__(self) -> str:
        columns = [f'{row}={getattr(self, row)}' for row in self.__table__.columns.keys()]
        return f"<{self.__class__.__name__}: {', '.join(columns)}>"
