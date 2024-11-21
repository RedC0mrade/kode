from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.authentication.actions import current_auth_user
from app.db_core.engine import db_helper
from app.messages.schema import Message
from app.users.schema import User
from app.messages import crud


messages_router = APIRouter(prefix="/messages", tags=["Message"])

@messages_router.get("/{ticket_id}", response_model=List[Message])
async def get_messages_from_ticket(ticket_id: int,
                                   user: User = Depends(current_auth_user),
                                   session: AsyncSession = db_helper.session_dependency):
    return await crud.get_messages(ticket_id=ticket_id, user=user, session=session)