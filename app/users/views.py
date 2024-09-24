from typing import Union
from fastapi import APIRouter, HTTPException, Response, Request, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from users.user_model_db import UserAlchemyModel
from users import crud
from users.schema import UserBase, UserCreate, UserPatch, UserPut
from db_core.engine import db_helper


@app.get("/users", response_model=list[UserBase])
async def get_users(
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    return await crud.get_users(session=session)


@app.get("/user/{user_id}", response_model=UserBase)
async def get_user(
    user_id: int, 
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    user = await crud.get_user(session=session, user_id=user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with {user_id}, not found"
        )


@app.post("/user", response_model=UserBase)
async def create_user(
    user_create: UserCreate, 
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    return await crud.create_user(session=session, user_in=user_create)


@app.api_route("/user{user_id}", 
               methods=["PUT", "PATCH"], 
               response_model=UserBase)
async def put_patsh_user(
    user_id: int,
    user_in: Union[UserBase, UserPatch],
    session: AsyncSession = Depends(db_helper.session_dependency)
    ):
    if Request.method == "PUT":
        return await crud.put_user(session=session, user_id=user_id, user_in=user_in[0])
    return await crud.patch_user(session=session, user_id=user_id, user_in=user_in[1])


@app.delete("/user/{user_id}")
async def delete_user(
    user_id: int, 
    session: AsyncSession = Depends(db_helper.session_dependency)
    ):
    try: 
        await crud.delete_user(session=session, user_id=user_id)
        return Response(status_code=200, content="user delete")
    except:
        return Response(status_code=404, content="user not found")
    