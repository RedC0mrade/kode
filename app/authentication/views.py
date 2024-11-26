from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import InvalidTokenError

from app.users.schema import User
from app.authentication.models import Token
from app.authentication.actions import (user_validate, 
                                         create_acces_token, 
                                         refresh_token)
from app.constant import REFRESH_TOKEN_TYPE, TOKEN_TYPE
from app.authentication.token_utils import decoded_token
from app.authentication.actions import oauth2_scheme
from app.users.user_model_db import UserAlchemyModel

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=Token)
def user_login(user: User = Depends(user_validate)) -> Token:
    
    create = create_acces_token(user)
    refresh = refresh_token(user)
    token = Token(access_token=create, refresh_token=refresh)
    return token


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decoded_token(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE)
    if current_token_type == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail=f"invalid token type {current_token_type!r} expected {token_type!r}")


async def get_user_by_token_sub(payload: dict, session: AsyncSession) -> User:
    username: str | None = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="token invalid (user not found)")        
    stmt = select(UserAlchemyModel).where(UserAlchemyModel.username==username)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="ivalid username")
    
    return user

class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(self, payload: dict = Depends(get_current_token_payload)):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)
        



get_current_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


@auth_router.post("/refresh", response_model=Token, response_model_exclude_none=True)
def user_refresh(user: User = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE))):
    access_token = create_acces_token(user)
    return Token(access_token=access_token)