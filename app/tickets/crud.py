from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from app.users.schema import UserWithId
from app.users.user_model_db import UserAlchemyModel
from app.tickets.schema import CreateTicket, Ticket
from app.tickets.ticket_model_db import TicketAlchemyModel


async def get_my_tasks(user: UserWithId, 
                       session: AsyncSession) -> List[TicketAlchemyModel]:
    stmt = select(TicketAlchemyModel).where(TicketAlchemyModel.executor_id==user.id)
    result: Result = await session.execute(stmt)
    tickets = result.scalars().all()
    return list(tickets)


async def get_my_tickets(user: UserWithId, 
                         session: AsyncSession) -> List[TicketAlchemyModel]:
    stmt = select(TicketAlchemyModel).where(TicketAlchemyModel.acceptor_id==user.id)
    result: Result = await session.execute(stmt)
    tickets = result.scalars().all()
    return list(tickets)


async def create_ticket(ticket_in: CreateTicket,
                        user: UserWithId,
                        session: AsyncSession) -> TicketAlchemyModel:
    stmt = select(UserAlchemyModel).where(UserAlchemyModel.username==ticket_in.acceptor_username)
    result: Result = await session.execute(stmt)
    acceptor = result.scalar_one_or_none()

    if not acceptor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{ticket_in.acceptor_username}, not found"
            )
    
    ticket = TicketAlchemyModel(ticket_name=ticket_in.ticket_name,
                                message=ticket_in.message,
                                amount=ticket_in.amount,
                                acceptor_id=acceptor.id,
                                executor_id=user.id)
    session.add(ticket)
    await session.commit()
    await session.refresh(ticket)

    return ticket 

async def ticker_done(ticked_id: int, acceptor: UserWithId, session: AsyncSession) -> TicketAlchemyModel | None:
    stmt = select(TicketAlchemyModel.amount).where(TicketAlchemyModel.id==ticked_id, TicketAlchemyModel.acceptor_id==acceptor.id)
    result: Result  = await session.execute(stmt)
    ticket: int = result.scalar_one_or_none()
    if not ticket:
        return None
    elif ticket <= 1:
        await delete_ticket(ticket_id=ticked_id, session=session)
        return None
    
    ticket_done = update(TicketAlchemyModel).where(TicketAlchemyModel.id==ticked_id).values({"amount": ticket-1})
    await session.execute(ticket_done)
    await session.commit()
    refresh_ticket: TicketAlchemyModel = await session.get(TicketAlchemyModel, ticked_id)

    return refresh_ticket
    
    
    
        

async def delete_ticket(ticket_id, session):
    ticket: TicketAlchemyModel = await session.get(TicketAlchemyModel, ticket_id)
    await session.delete(ticket)
    await session.commit()
    