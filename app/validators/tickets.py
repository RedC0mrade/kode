from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tags.tag_model_db import TagAlchemyModel


async def validate_tags_in_base(tags: list | set, session: AsyncSession):
    stmt = select(TagAlchemyModel.id).where(TagAlchemyModel.id.in_(tags))
    result: Result = await session.execute(stmt)
    tags_in_base = result.scalars().all()
    
    mising_tags = [tag for tag in tags if tag not in tags_in_base]
    if mising_tags:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong tag id: {", ".join(map(str, mising_tags))}")