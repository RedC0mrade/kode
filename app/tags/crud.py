from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tags.schema import CreateTag, Tag
from app.tags.tag_model_db import TagAlchemyModel


async def get_all_tags(session: AsyncSession) -> list[TagAlchemyModel]:
    stmt = select(TagAlchemyModel)
    result: Result = await session.execute(stmt)
    tags = result.scalars().all()
    return list(tags)


async def create_tag(tag_in: CreateTag,
                     session: AsyncSession) -> TagAlchemyModel:
    tag = TagAlchemyModel(tag_name=tag_in.tag_name,
                          tag_color=tag_in.tag_color)
    session.add(tag)
    await session.commit()
    return tag