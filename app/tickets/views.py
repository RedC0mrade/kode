from fastapi import APIRouter, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from app.tickets.schema import Ticket, CreateTicket
from app.users.schema import UserWithId
from app.authentication.actions import current_auth_user
from app.db_core.engine import db_helper
from app.tickets import crud

ticket_router = APIRouter(prefix="/ticket_router", tags=["ticket"])

@ticket_router.post("/", response_model=CreateTicket, status_code=201)
async def create_ticket(ticket_in: CreateTicket,
                        user: UserWithId = Depends(current_auth_user),
                        session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_ticket(ticket_in=ticket_in, user=user, session=session)


@ticket_router.delete("/{ticket_id}", status_code=204)
async def delete_ticket(ticket_id: int, 
                        session: AsyncSession = Depends(db_helper.session_dependency)):
    
    try: 
        await crud. delete_ticket(ticket_id=ticket_id, session=session)
    except:
        return Response(status_code=404, content="user not found")
