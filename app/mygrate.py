import asyncio
from alembic import command
from alembic.config import Config
from db_core.engine import db_helper

async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    async with db_helper.engine.begin() as conn:
        await command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    asyncio.run(run_migrations())