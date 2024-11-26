from datetime import timedelta
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_core.engine import db_helper
from app.users.user_model_db import UserAlchemyModel
from app.users.schema import User
from app.authentication.password_utils import validate_password
from app.authentication.token_utils import encode_token, decoded_token
from app.constant import TOKEN_TYPE, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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


async def current_auth_user(
        session: AsyncSession = Depends(db_helper.session_dependency),
        token: str = Depends(oauth2_scheme)
        ) -> User:
    try:
        payload: dict = decoded_token(token=token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    username: str | None = payload.get("username")

    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user not found")
    
    stmt = select(UserAlchemyModel).where(UserAlchemyModel.username==username)
    result: Result = await session.execute(stmt)
    user = result.scalar_one()
    return user


def create_token(token_type: str, 
                 token_data: dict, 
                 expire_minutes: int = settings.access_token_expire_minute,
                 expire_timedelta: timedelta | None = None) ->str:
    
    payload = {TOKEN_TYPE: token_type}
    payload.update(token_data)
    
    token = encode_token(payload=payload, 
                         expire_minutes=expire_minutes, 
                         expare_time_delta=expire_timedelta)
    return  token

def refresh_token(user: User) -> str:
    payload = {"sub": user.username}
    token = create_token(token_type=REFRESH_TOKEN_TYPE, 
                         token_data=payload, 
                         expire_timedelta=timedelta(days=settings.access_token_refresh_days))
    return token


def create_acces_token(user: User) -> str:

    payload = {"sub": user.username,
               "username": user.username,
               "email": user.email}
 
    token = create_token(token_type=ACCESS_TOKEN_TYPE, 
                         token_data=payload,
                         expire_minutes=settings.access_token_expire_minute)
    return token
