from fastapi import APIRouter, Depends

from app.users.schema import User
from app.authentication.models import Token
from app. authentication.actions import user_validate


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=Token)
def user_login(user: User = Depends(user_validate)) -> Token:
    
    create_token = create_token(user)
    refresh_token = refresh_token(user)
    return Token(access_token=create_token, refresh_token=refresh_token)
