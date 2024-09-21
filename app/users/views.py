from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import async_scoped_session

from main import app
from app.users.user_model_db import UserAlchemyModel
from app.users import crud
from app.users.schema import UserBase, UserCreate


session = async_scoped_session()


@app.get("/users", response_model=list[UserBase])
async def get_users(session):
    return await crud.get_users(session=session)


@app.get("/user/{user_id}", response_model=UserBase)
async def get_user(session, user_id: int):
    user = await crud.get_user(session=session, user_id=user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with {user_id}, not founf"
        )

@app.post("/user", response_model=UserBase)
async def create_user(session, user_create: UserCreate):
    return await crud.create_user(session=session, user_in=user_create)
