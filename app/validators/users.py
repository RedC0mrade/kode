from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.users.schema import User, UserWithId
from app.users.user_model_db import UserAlchemyModel

async def validate_user(user_id: int,
                        session: AsyncSession) -> UserAlchemyModel:
    
    searched_user: UserAlchemyModel | None = await session.get(UserAlchemyModel, user_id)

    if not searched_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")
    
    return searched_user


async def validete_unauthenticated_user(user: User = Depends(current_auth_user)) -> None:
    print(user)
    if user:
        raise HTTPException(status_code=403, detail="You are already authenticated.")