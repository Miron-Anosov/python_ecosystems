""""Здесь проходит работа с БД"""
from typing import Iterable

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import delete, select, create_engine

URL_DB = 'sqlite+pysqlite:///emails.db'

engine_ = create_engine(url=URL_DB)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class SubscribeEmails(Base):
    __tablename__ = 'emails'

    email: Mapped[str] = mapped_column(unique=True, nullable=False)


SubscribeEmails.metadata.create_all(bind=engine_)
session = sessionmaker(bind=engine_)


def subscribe(email: str):
    """
    Пользователь указывает почту и подписывается на рассылку.
    Каждую неделю ему будет приходить письмо о сервисе на почту.
    """
    with session() as conn:
        email = SubscribeEmails(email=email)
        conn.add(email)
        conn.commit()


def get_emails_for_subscribe() -> Iterable[SubscribeEmails]:
    """Рассылка сообщений по подписке на почту."""
    with session() as conn:
        return conn.execute(select(SubscribeEmails)).scalars().all()


def del_email(email: str) -> None:
    """
    Пользователь указывает почту и отписывается от рассылки.
    """
    with session() as conn:
        conn.execute(delete(SubscribeEmails).where(SubscribeEmails.email == email))
        conn.commit()
