from typing import List
from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tags.tag_model_db import TicketTagAssociation, TagAlchemyModel


async def validate_tags_in_base(tags: list | set, session: AsyncSession):
    stmt = select(TagAlchemyModel.id).where(TagAlchemyModel.id.in_(tags))
    result: Result = await session.execute(stmt)
    tags_in_base = result.scalars().all()
    
    mising_tags = [tag for tag in tags if tag not in tags_in_base]
    if mising_tags:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Wrong tag id: {", ".join(map(str, mising_tags))}")
    
    
async def validate_assosiation(assosiation_id: int, session: AsyncSession) -> TicketTagAssociation:
    assosiation = await session.get(TicketTagAssociation, assosiation_id)

    if not assosiation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Association {assosiation_id} not found")
    return assosiation


async def validate_tag(tag_id: int, session: AsyncSession) -> TagAlchemyModel:
    tag = await session.get(TagAlchemyModel, tag_id)

    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tag {tag_id} not found")
    return tag


# async def validate_all_associatons(ticket_id: int, session: AsyncSession) -> List[TicketTagAssociation]:
#     stmt = select(TicketTagAssociation).where(TicketTagAssociation.ticket_id==ticket_id)
#     result: Result = await session.execute(stmt)
#     associatons = result.scalars().all()
#     if not associatons:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Association in ticket withs {ticket_id} not found")
#     return list(associatons)