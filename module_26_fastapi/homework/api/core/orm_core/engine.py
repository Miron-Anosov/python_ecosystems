from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine
from asyncio import current_task


class AsyncCoreDB:
    def __init__(self, url: str, echo: bool):
        self.async_engine = create_async_engine(url=url, echo=echo)
        self.async_session_maker = async_sessionmaker(bind=self.async_engine,
                                                      expire_on_commit=False,
                                                      autoflush=False,
                                                      autocommit=False,
                                                      )

        self.async_scoped_session = async_scoped_session(
                    session_factory=self.async_session_maker,
                    scopefunc=current_task
                )

    def get_async_scoped_session(self):
        return self.async_scoped_session()
