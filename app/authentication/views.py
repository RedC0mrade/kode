from fastapi import APIRouter, Depends

from app.users.schema import User
from app.authentication.models import Token
from app. authentication.actions import (user_validate, 
                                         create_acces_token, 
                                         refresh_token)


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=Token)
def user_login(user: User = Depends(user_validate)) -> Token:
    
    create = create_acces_token(user)
    refresh = refresh_token(user)
    token = Token(access_token=create, refresh_token=refresh)
    return token
