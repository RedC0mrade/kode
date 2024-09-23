from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from users.user_model_db import UserAlchemyModel
from users import crud
from users.schema import UserBase, UserCreate
from db_core.engine import db_helper


@app.get("/users", response_model=list[UserBase])
async def get_users(
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    return await crud.get_users(session=session)


@app.get("/user/{user_id}", response_model=UserBase)
async def get_user(
    user_id: int, 
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    user = await crud.get_user(session=session, user_id=user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with {user_id}, not found"
        )


@app.post("/user", response_model=UserBase)
async def create_user(
    user_create: UserCreate, 
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    return await crud.create_user(session=session, user_in=user_create)


@app.delete("/user/{user_id}")
async def delete_user(
    user_id: int, 
    session: AsyncSession = Depends(db_helper.session_dependency)
    ):
    await crud.delete_user(session=session, user_id=user_id)
    # try:
    #     return message
    # except:
    #     raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"He can't be delete. User with {user_id}, not found. "
    #     )