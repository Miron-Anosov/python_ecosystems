from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey, DateTime


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        columns = [
            f"{row}={getattr(self, row)}" for row in self.__table__.columns.keys()
        ]

        return f"<{self.__class__.__tablename__}> {','.join(columns)}"


class Client(Base):

    __tablename__ = "client"

    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    surname: Mapped[str] = mapped_column(String(length=50), nullable=False)
    credit_card: Mapped[str | None] = mapped_column(String(length=50))
    car_number: Mapped[str | None] = mapped_column(String(length=10))


class Parking(Base):

    __tablename__ = "parking"

    address: Mapped[str] = mapped_column(String(length=100))
    opened: Mapped[bool | None]
    count_places: Mapped[int]
    count_available_places: Mapped[int]


class ClientParking(Base):

    __tablename__ = "client_parking"

    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), unique=True)

    parking_id: Mapped[int] = mapped_column(ForeignKey("parking.id"), unique=True)

    time_in: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    time_out: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


db = SQLAlchemy(model_class=Base)
