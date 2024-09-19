from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base


engine = create_async_engine("sqlite+aiosqlite://", echo=True)

async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


