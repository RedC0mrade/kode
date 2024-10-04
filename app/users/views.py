from fastapi import HTTPException, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from users.user_model_db import UserAlchemyModel
from users import crud
from users.schema import User, UserBase, UserPatch
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
        detail=f"User with {user_id} id's, not found"
        )


@app.post("/user", response_model=UserBase)
async def create_user(
    user_create: User, 
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    return await crud.create_user(session=session, user_in=user_create)


@app.put("/user/{user_id}", response_model=User)
async def put_user(user_id: int,
                   user_in: User,
                   session: AsyncSession = Depends(db_helper.session_dependency),
                   ):
    result: dict = await crud.put_user(user_id=user_id, session=session, user_in=user_in)
    return Response(status_code=200, content=f"data changed {result}")


@app.patch("/user/{user_id}", response_model=User)
async def patch_user(
    user_id: int,
    user_in:  UserPatch,
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    result: dict = await crud.patch_user(session=session, user_id=user_id, user_in=user_in)
    return Response(status_code=200, content=f"data changed {result}")

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
    