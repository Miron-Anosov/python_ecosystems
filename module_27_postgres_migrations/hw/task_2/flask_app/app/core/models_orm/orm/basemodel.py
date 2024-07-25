# Базовая модель sqlalchemy для работы с ORM. Переопределен __repr__ для удобного представления моделей.
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __abstract__ = True

    def __repr__(self) -> str:
        columns = [
            f"{row}={getattr(self, row)}"
            for row in self.__table__.columns.keys()
        ]

        return f"<{self.__class__.__tablename__}> {','.join(columns)}"
