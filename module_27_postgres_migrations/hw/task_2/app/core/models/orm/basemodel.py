from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __abstract__ = True

    def __repr__(self) -> str:
        columns = [
            f"{row}={getattr(self, row)}"
            for row in self.__table__.columns.key()
        ]

        return f"<{self.__class__.__tablename__}> {','.join(columns)}"
