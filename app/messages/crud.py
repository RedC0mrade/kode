from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schema import UserWithId
from app.validators.tickets import validate_ticket


async def get_messages(ticket_id: int, user: UserWithId, session: AsyncSession):
    ticket = await validate_ticket(ticket_id=ticket_id, session=session)

    if ticket.acceptor_id == user.id or ticket.executor_id == user.id:
        return ticket.messages

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with {user.id} not found")
