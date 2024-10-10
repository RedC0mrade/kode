from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


auth_router = APIRouter(prefix="/auth", tags=["auth"])

security = HTTPBasic()
@auth_router.get("/")
def authentication(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"usernаme": credentials.usernamename, "password": credentials.password}