import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from db_core.base import Base
from db_core.engine import db_helper
from users.user_model_db import UserAlchemyModel
from users import views


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
# app.include_router(user_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
