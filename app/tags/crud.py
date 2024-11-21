from fastapi import HTTPException
from sqlalchemy import Result, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tags.schema import CreateTag, Tag
from app.tags.tag_model_db import TagAlchemyModel, TicketTagAssociation
from app.validators.tags import validate_assosiation, validate_tag


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


async def delete_tag(tag_id: int, session: AsyncSession) -> None:
    tag: TagAlchemyModel = await validate_tag(
        tag_id=tag_id,
        session=session)
    await session.delete(tag)
    await session.commit()


async def delete_association(association_id: int, session: AsyncSession) -> None:
    association: TicketTagAssociation = await validate_assosiation(
        assosiation_id=association_id, 
        session=session)
    await session.delete(association)
    await session.commit()


async def delete_all_associatons_in_ticket(ticket_id: int, 
                                           session: AsyncSession) -> None:
    stmt = delete(TicketTagAssociation).where(TicketTagAssociation.ticket_id == ticket_id)
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404, 
            detail=f"No associations found for ticket_id {ticket_id}")