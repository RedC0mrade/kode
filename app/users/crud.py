from typing import List, Optional

from fastapi import Response
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from users.user_model_db import UserAlchemyModel
from users.schema import User, UserBase, UserPatch


async def get_users(session: AsyncSession) -> List[UserAlchemyModel]:
    """Get users list"""
    stmt = select(UserAlchemyModel)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int) -> UserAlchemyModel | None:
    """Get User"""
    return await session.get(UserAlchemyModel, user_id)


async def create_user(session: AsyncSession, user_in: UserBase) -> UserAlchemyModel:
    """Create User"""
    new_user = UserAlchemyModel(**user_in.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user


async def put_user(session: AsyncSession, user_in: User, user_id: int) -> UserAlchemyModel:
    """Put User"""
    user: UserAlchemyModel = await session.get(UserAlchemyModel, user_id)
    new_values: dict = user_in.model_dump()
    for name, attr in new_values.items():
        setattr(user, name, attr)
    await session.commit()
    return user


async def patch_user(session: AsyncSession, user_in: UserPatch, user_id: int):
    """Patch User"""
    user: UserAlchemyModel = await session.get(UserAlchemyModel, user_id)
    new_values: dict = user_in.model_dump(exclude_unset=True)
    for name, attr in new_values.items():
        setattr(user, name, attr)
    await session.commit()
    return user
    

async def delete_user(session: AsyncSession, user_id: int):
    """Delete user"""
    del_user = await session.get(UserAlchemyModel, user_id)
    await session.delete(del_user)
    await session.commit()
