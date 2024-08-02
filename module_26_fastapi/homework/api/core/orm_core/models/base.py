from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseORM(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def __repr__(self) -> str:
        columns = [
            f'{row}={getattr(self, row)}'
            for row in self.__table__.columns.keys()
        ]

        return f"<{self.__class__.__name__}: {', '.join(columns)}>"
