from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.messages.message_model_db import MessageAlchemyModel
from app.tickets.ticket_model_db import TicketAlchemyModel
from app.users.schema import UserWithId
from app.validators.messges import validate_message
from app.validators.tickets import validate_ticket


async def get_messages(ticket_id: int,
                       user: UserWithId,
                       session: AsyncSession) -> List[MessageAlchemyModel]:

    ticket: TicketAlchemyModel = await validate_ticket(ticket_id=ticket_id,
                                                       user=user,
                                                       session=session)
    
    return list(ticket.messages)


async def delete_message(message_id: int,
                         user: UserWithId,
                         session: AsyncSession) -> None:

    message = await validate_message(message_id=message_id,
                                     user=user,
                                     session=session)
    
    await session.delete(message)
    await session.commit()


async def delete_all_messages(ticket_id: int,
                              user: UserWithId,
                              session: AsyncSession) -> TicketAlchemyModel:

    ticket: TicketAlchemyModel = await validate_ticket(ticket_id=ticket_id, session=session)
    if ticket.executor_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"You can't delete messages {ticket_id} id's")
    ticket.messages.clear()
    await session.commit()
    return ticket


async def add_message(ticket_id: int,
                      user: UserWithId,
                      message: str,
                      session: AsyncSession) -> MessageAlchemyModel:
    
    await validate_ticket(ticket_id=ticket_id,
                          user=user,
                          session=session)
    
    message = MessageAlchemyModel(message=message, ticket_id=ticket_id)
    session.add(message)
    await session.commit()
    return message


async def update_message(message_id: int,
                         message_text: str,
                         session: AsyncSession,
                         user: UserWithId):
    
    message: MessageAlchemyModel = await validate_message(message_id=message_id, user=user, session=session)
    message.message = message_text
    session.add(message)
    await session.commit()
    return message