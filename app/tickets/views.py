from typing import List
from fastapi import APIRouter, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from app.tickets.schema import Ticket, CreateTicket, TicketName
from app.users.schema import UserWithId
from app.authentication.actions import current_auth_user
from app.db_core.engine import db_helper
from app.tickets import crud

ticket_router = APIRouter(prefix="/ticket_router", tags=["ticket"])

@ticket_router.post("/", response_model=Ticket, status_code=201)
async def create_ticket(ticket_in: CreateTicket,
                        ticket_name: TicketName,
                        user: UserWithId = Depends(current_auth_user),
                        session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_ticket(ticket_in=ticket_in, user=user, ticket_name=ticket_name, session=session)


@ticket_router.delete("/{ticket_id}", status_code=204)
async def delete_ticket(ticket_id: int, 
                        session: AsyncSession = Depends(db_helper.session_dependency)):
    
    try: 
        await crud.delete_ticket(ticket_id=ticket_id, session=session)
    except:
        return Response(status_code=404, content="Ticket not found")
    

@ticket_router.get("/my_tickets", response_model=List[Ticket])
async def get_my_tickets(user: UserWithId = Depends(current_auth_user),
                         session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_my_tickets(user=user, session=session)


@ticket_router.get("/my_tasks", response_model=List[Ticket])
async def get_my_tickets(user: UserWithId = Depends(current_auth_user),
                         session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_my_tasks(user=user, session=session)


@ticket_router.post("/ticket_done/{ticked_id}", response_model=Ticket | None)
async def ticket_done(ticket_id: int,
                      acceptor: UserWithId = Depends(current_auth_user),
                      session: AsyncSession = Depends(db_helper.session_dependency)):
    
    return await crud.ticker_done(ticket_id, acceptor=acceptor, session=session)


@ticket_router.post("/add_to_existing_ticket/{ticked_id}", response_model=Ticket)
async def add_to_existing_tickets(ticket_id: int,
                                  amount: int,
                                  message: str,
                                  executor: UserWithId = Depends(current_auth_user),
                                  session: AsyncSession = Depends(db_helper.session_dependency)):
    
    return await crud.add_to_existing_tickets(ticket_id=ticket_id,
                                              amount=amount,
                                              message=message,
                                              executor=executor,
                                              session=session)


@ticket_router.get("/ticket", response_model=Ticket)
async def get_ticket(ticket_id: int,
                     session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_ticket(ticket_id=ticket_id, session=session)