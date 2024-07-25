from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, ForeignKey, BOOLEAN

from .basemodel import BaseModel

if TYPE_CHECKING:
    from .coffee import CoffeeORM # noqa


class UserORM(BaseModel):
    """
    CREATE TABLE users (
    id SERIAL NOT NULL,
    name VARCHAR(50) NOT NULL,
    has_sale BOOLEAN,
    address JSON,
    coffee_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(coffee_id) REFERENCES coffee (id)
    )
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    has_sale: Mapped[bool] = mapped_column(BOOLEAN, nullable=True)
    address: Mapped[dict] = mapped_column(JSON, nullable=True)
    coffee_id: Mapped[int] = mapped_column(ForeignKey('coffee.id'))
    prefer_kind_of_coffee: Mapped["CoffeeORM"] = relationship(back_populates="type_coffee")
