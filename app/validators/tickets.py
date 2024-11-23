from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tickets.ticket_model_db import TicketAlchemyModel


async def validate_ticket(ticket_id: int, session: AsyncSession) -> TicketAlchemyModel:

    ticket: TicketAlchemyModel = await session.get(TicketAlchemyModel, ticket_id)

    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ticket whis {ticket_id} not found")
    
    return ticket