import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from alembic import command
from alembic.config  import Config


alembic_conf = Config("alembic.ini")
command.upgrade(alembic_conf, "head")

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
