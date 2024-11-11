from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.tags.schema import CreateTag, Tag
from app.db_core.engine import db_helper
from app.tags import crud


tag_router = APIRouter(prefix="/tag_router", tags=["tags"])

@tag_router.get("/", response_model=List[Tag])
async def get_all_tags(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_all_tags(session=session)


@tag_router.post("/create_tag", response_model=Tag)
async def create_tag(tag_in: CreateTag,
                     session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_tag(session=session, tag_in=tag_in)