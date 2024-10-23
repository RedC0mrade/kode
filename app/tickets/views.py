from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.tickets.schema import Ticket, CreateTicket
from app.users.schema import UserWithId
from app.authentication.actions import current_auth_user
from app.db_core.engine import db_helper
from app.tickets import crud

ticket_router = APIRouter(prefix="/ticket_router", tags=["ticket"])

@ticket_router.post("/", response_model=CreateTicket, status_code=201)
def create_ticket(ticket_in: CreateTicket,
                  user: UserWithId = Depends(current_auth_user),
                  session: AsyncSession = Depends(db_helper.session_dependency)):
    return crud.create_ticket(ticket_in=ticket_in, user=user, session=session)