from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.messages.message_model_db import MessageAlchemyModel
from app.messages.schema import Message
from app.tickets.ticket_model_db import TicketAlchemyModel
from app.users.schema import UserWithId
from app.validators.tickets import validate_ticket


async def get_messages(ticket_id: int, user: UserWithId, session: AsyncSession) -> List[MessageAlchemyModel]:

    ticket = await validate_ticket(ticket_id=ticket_id, session=session)
    if ticket.acceptor_id == user.id or ticket.executor_id == user.id:
        return list(ticket.messages)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with {user.id} not found")


async def delete_message(message_id: int, session: AsyncSession) -> None:
    message: MessageAlchemyModel | None = await session.get(MessageAlchemyModel, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Message with {message_id} not found")
    
    await session.delete(message)
    await session.commit()


async def delete_all_messages(ticket_id: int, user: UserWithId, session: AsyncSession) -> TicketAlchemyModel:

    ticket = await validate_ticket(ticket_id=ticket_id, session=session)
    if ticket.executor_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"You can't delete messages in ticket {ticket_id} id's")
    ticket.messages.clear()
    await session.commit()
    return ticket


async def add_message(ticket_id: int, message: str, session: AsyncSession) -> MessageAlchemyModel:
    
    await validate_ticket(ticket_id=ticket_id, session=session)
    message = MessageAlchemyModel(message=message, ticket_id=ticket_id)
    session.add(message)
    await session.commit()
    return message
