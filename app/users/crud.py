from typing import List

from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_model_db import UserAlchemyModel
from app.users.schema import User, UserWithId, UserPatch
from app.authentication.password_utils import hash_password


async def get_users(session: AsyncSession) -> List[UserAlchemyModel]:

    stmt = select(UserAlchemyModel)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int) -> UserAlchemyModel | None:
    
    return await session.get(UserAlchemyModel, user_id)


async def create_user(session: AsyncSession, user_in: UserWithId) -> UserAlchemyModel:

    user_in.password = hash_password(user_in.password)
    new_user = UserAlchemyModel(**user_in.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user


async def put_user(session: AsyncSession, user_in: User, user_id: int) -> dict:
    
    user_in.password = hash_password(user_in.password)
    new_values: dict = user_in.model_dump()
    user = update(UserAlchemyModel).where(UserAlchemyModel.id==user_id).values(new_values)
    await session.execute(user)
    await session.commit()
    return new_values


async def patch_user(session: AsyncSession, user_in: UserPatch, user_id: int) -> dict:
    
    new_values: dict = user_in.model_dump(exclude_unset=True)
    if new_values.get("password"):
        new_values["password"] = hash_password(user_in.password)
    user = update(UserAlchemyModel).where(UserAlchemyModel.id==user_id).values(new_values)
    await session.execute(user)
    await session.commit()
    return new_values
    

async def delete_user(session: AsyncSession, user_id: int) -> None:

    user = await session.get(UserAlchemyModel, user_id)
    await session.delete(user)
    await session.commit()

