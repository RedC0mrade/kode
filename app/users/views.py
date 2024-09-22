from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from app.users.user_model_db import UserAlchemyModel
from app.users import crud
from app.users.schema import UserBase, UserCreate
from app.db_core.engine import db_helper


@app.get("/users", response_model=list[UserBase])
async def get_users(
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    return await crud.get_users(session=session)


@app.get("/user/{user_id}", response_model=UserBase)
async def get_user(
    user_id: int, 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
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
    session:AsyncSession = Depends(db_helper.scoped_session_dependency),
    ):
    return await crud.create_user(session=session, user_in=user_create)
