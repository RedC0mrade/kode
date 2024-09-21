from asyncio import current_task
from pathlib import Path
from sqlalchemy.ext.asyncio import (AsyncSession, 
                                    async_sessionmaker, 
                                    create_async_engine, 
                                    async_scoped_session)


BASE_DIR = Path(__file__).parent.parent.parent
DB_URL = f"sqlite+aiosqlite:///{BASE_DIR}/JuliaBars.sqlite3"

# engine = create_async_engine(DB_URL, echo=True)
# session_factory = async_sessionmarker(
#     bind=engine,
#     autoflush=False,
#     autocommit=False,
#     expere_on_commit=False,
#     )
# async def scooped_session_dependency(session_factory):
# session = async_scoped_session(session_factory=session_factory, scopefunc=current_task)

class DatabaseHelper:
    def __init__(self, url: str = DB_URL, echo: bool = True):
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
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper()