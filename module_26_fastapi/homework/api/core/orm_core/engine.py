from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


class AsyncCoreDB:
    def __init__(self, url: str, echo: bool):
        self.async_engine = create_async_engine(url=url, echo=echo)
        self.create_async_session_maker = async_sessionmaker(bind=self.async_engine,
                                                             expire_on_commit=False,
                                                             autoflush=False,
                                                             autocommit=False,
                                                             )
