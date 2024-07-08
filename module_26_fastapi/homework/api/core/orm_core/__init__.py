from .crud import crud
from .engine import AsyncCoreDB
from ..settings import settings
from .models.base import BaseORM


def create_engine(url: str = settings.host_database_sqlalchemy, echo: bool = settings.ECHO) -> AsyncCoreDB:
    return AsyncCoreDB(url=url, echo=echo)


engine = create_engine()

__all__ = ['engine', 'crud', 'BaseORM']
