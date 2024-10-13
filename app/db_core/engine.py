from asyncio import current_task
from sqlalchemy.ext.asyncio import (AsyncSession, 
                                    async_sessionmaker, 
                                    create_async_engine, 
                                    async_scoped_session)

from config import settings
print(settings.url)


class DatabaseHelper:
    def __init__(self, url: str = settings.url, echo: bool = True):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()

db_helper = DatabaseHelper()