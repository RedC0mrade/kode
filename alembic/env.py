import asyncio
from logging.config import fileConfig

from sqlalchemy import pool

from alembic import context
from app.db_core.base import Base
from app.db_core.engine import DB_URL, db_helper


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

async def run_migrations_online():
    async with db_helper.engine.connect() as connection:
        await connection.run_sync(context.configure, 
            target_metadata=target_metadata,
            compare_type=True
        )

        async with connection.begin():
            context.run_migrations()

def run_migrations():
    asyncio.run(run_migrations_online())

def run_migrations_offline():
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations()