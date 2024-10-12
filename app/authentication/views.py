from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from authentication.token_utils import encode_token
from authentication.password_utils import validate_password
from users.user_model_db import UserAlchemyModel
from db_core.engine import db_helper
from users.schema import User
from models import Token

auth_router = APIRouter(prefix="/auth", tags=["auth"])

async def user_validate(session: AsyncSession = Depends(db_helper.session_dependency), 
                        username: str = Form(), 
                        password: str = Form()):
    
    user = await session.get(UserAlchemyModel, username=username)
    print(user)
    
    auth_rxp = HTTPException(status_code=status.HTTP_401,
                             detail="ivalid ussername or password")




@auth_router.post("/login", response_model=Token)
def user_login(user: User = Depends(user_validate)):
    
    payload = {"sub": user.username,
               "username": user.username,
               "email": user.email}
    
    token = encode_token(payload)

    return Token(acceess_token=token, token_type="Bearer")