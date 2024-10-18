from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import crud
from app.users.schema import User, UserWithId, UserPatch
from app.db_core.engine import db_helper
from app.authentication.actions import current_auth_user


router_user = APIRouter(prefix="/user", tags=["user"])
router_users = APIRouter(prefix="/users", tags=["users"])

@router_users.get("/", response_model=list[UserWithId])
async def get_users(
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    return await crud.get_users(session=session)


@router_user.get("/me", response_model=UserWithId)
def get_me(user: User = Depends(current_auth_user)):
    return user


@router_user.get("/{user_id}", response_model=UserWithId)
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


@router_user.post("/", response_model=UserWithId, status_code=201)
async def create_user(
    user_create: User, 
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    return await crud.create_user(session=session, user_in=user_create)



@router_user.put("/{user_id}", response_model=User)
async def put_user(
    user_id: int,
    user_in: User,
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    result: dict = await crud.put_user(user_id=user_id, session=session, user_in=user_in)
    return Response(status_code=200, content=f"data changed {result}")


@router_user.patch("/{user_id}", response_model=User)
async def patch_user(
    user_id: int,
    user_in:  UserPatch,
    session: AsyncSession = Depends(db_helper.session_dependency),
    ):
    result: dict = await crud.patch_user(session=session, user_id=user_id, user_in=user_in)
    return Response(status_code=200, content=f"data changed {result}")


@router_user.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int, 
    session: AsyncSession = Depends(db_helper.session_dependency)
    ):
    try: 
        await crud.delete_user(session=session, user_id=user_id)
    except:
        return Response(status_code=404, content="user not found")
    