from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.tags.schema import CreateTag, Tag
from app.db_core.engine import db_helper
from app.tags import crud


tag_router = APIRouter(prefix="/tag_router", tags=["tags"])
association_router = APIRouter(prefix="/association_router", tags=["association_router"])

@tag_router.get("/", response_model=List[Tag])
async def get_all_tags(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_all_tags(session=session)


@tag_router.post("/create_tag", response_model=Tag)
async def create_tag(tag_in: CreateTag,
                     session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_tag(session=session, tag_in=tag_in)


@tag_router.delete("/{tag_id}", status_code=204)
async def delete_tag(tag_id: int, 
                        session: AsyncSession = Depends(db_helper.session_dependency)):
    
    try: 
        await crud.delete_tag(tagt_id=tag_id, session=session)
    except:
        return Response(status_code=404, content="tag not found")
    

@association_router.delete("/{association_id}", status_code=204)
async def delete_association(association_id: int, 
                             session: AsyncSession = Depends(db_helper.session_dependency)):
    
    try: 
        await crud.delete_association(association_id=association_id, session=session)
    except:
        return Response(status_code=404, content="association not found")
