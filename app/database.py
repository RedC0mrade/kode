# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy.orm import Session, sessionmaker
# from sqlalchemy import URL, create_engine, text
# from config import settings

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
#from config import DATABASE_URL
#from models import Base
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine(
#     url=settings.DATABASE_URL_asyncpg,
#     echo=True,
#     # pool_size=5,
#     # max_overflow=10
#     )

engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname", echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        # Создаем все таблицы
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res}")
        await conn.run_sync(declarative_base().metadata.create_all)
