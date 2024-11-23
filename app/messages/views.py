from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.authentication.actions import current_auth_user
from app.db_core.engine import db_helper
from app.messages.schema import Message
from app.tickets.schema import Ticket
from app.users.schema import User
from app.messages import crud


messages_router = APIRouter(prefix="/messages", tags=["Message"])

@messages_router.get("/{ticket_id}", response_model=list[Message])
async def get_messages_from_ticket(ticket_id: int,
                                   user: User = Depends(current_auth_user),
                                   session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_messages(ticket_id=ticket_id, user=user, session=session)


@messages_router.delete("/{message_id}", status_code=204)
async def delete_message(message_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.delete_message(message_id=message_id, session=session)


@messages_router.delete("/all/{ticket_id}", response_model=Ticket)
async def delete_all_messages(ticket_id: int,
                              user: User = Depends(current_auth_user),
                              session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.delete_all_messages(ticket_id=ticket_id, user=user, session=session)


@messages_router.post("/{message_id}", response_model=Message)
async def add_message(ticket_id: int, message: str, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.add_message(ticket_id=ticket_id, message=message, session=session)
