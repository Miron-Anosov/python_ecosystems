from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ARRAY

from .basemodel import BaseModel

if TYPE_CHECKING:
    from .user import UserORM  # noqa


class CoffeeORM(BaseModel):
    """
    СREATE TABLE coffee (
    id SERIAL NOT NULL,
    title VARCHAR(200) NOT NULL,
    origin VARCHAR(200),
    intensifier VARCHAR(100),
    notes VARCHAR[],
    PRIMARY KEY (id)
        )
    """
    __tablename__ = 'coffee'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=200), nullable=False)
    origin: Mapped[str] = mapped_column(String(length=200), nullable=True)
    intensifier: Mapped[str] = mapped_column(String(length=100), nullable=True)
    notes: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    type_coffee: Mapped[list["UserORM"]] = relationship(back_populates="prefer_kind_of_coffee")
