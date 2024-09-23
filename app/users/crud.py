"""
Create
Read
Update
Delete
"""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from users.user_model_db import UserAlchemyModel
from users.schema import UserCreate


async def get_users(session: AsyncSession) -> List[UserAlchemyModel]:
    """Get users list"""
    stmt = select(UserAlchemyModel)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int) -> UserAlchemyModel | None:
    """Get User"""
    return await session.get(UserAlchemyModel, user_id)


async def create_user(session: AsyncSession, user_in: UserCreate) -> UserAlchemyModel:
    """Create User"""
    new_user = UserAlchemyModel(**user_in.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user


async def delete_user(session: AsyncSession, user_id: int):
    """Delete user"""
    del_user = await session.get(UserAlchemyModel, user_id)
    await session.delete(del_user)
    await session.commit()
