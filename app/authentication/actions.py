from fastapi import Depends, Form, HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_core.engine import db_helper
from app.users.user_model_db import UserAlchemyModel
from app.users.schema import User
from app.authentication.password_utils import validate_password
from app.authentication.token_utils import encode_token


async def user_validate(session: AsyncSession = Depends(db_helper.session_dependency), 
                        username: str = Form(), 
                        password: str = Form()) -> UserAlchemyModel:
    
    stmt = select(UserAlchemyModel).where(UserAlchemyModel.username==username)
    result: Result = await session.execute(stmt)
    user: User = result.scalar_one_or_none()
    if not user:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="ivalid username")
    
    if not validate_password(password=password, hashed_password=user.password):

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="ivalid password")
    
    return user

def create_token(token_data: dict) ->str:
    payload = {}
    payload.update()
    

def create_token(user: User) -> str:

    payload = {"sub": user.username,
               "username": user.username,
               "email": user.email}
    
    token = encode_token(payload)

    return token   
def refresh_token(user: User) -> str:
    

