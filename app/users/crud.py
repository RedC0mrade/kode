"""
Create
Read
Update
Delete
"""
from typing import List

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from user_model import User


async def get_users(session: AsyncSession) -> List[User]:
    """Get users list"""
    stmt = select(User)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_users(session: AsyncSession, user_id: int) -> User | None:
    """Get User"""
    stmt = select(User).where(User.id == user_id)
    result: Result = await session.exxecut(stmt)
    user = result.scalars()
    return user
