from json import JSONDecodeError
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import and_, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from app.users.schema import UserWithId
from app.users.user_model_db import UserAlchemyModel
from app.tickets.schema import CreateTicket, Ticket, TicketName
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
                        ticket_name: TicketName,
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
    
    check_stmt = select(TicketAlchemyModel).where(and_(
        TicketAlchemyModel.acceptor_id==acceptor.id,
        TicketAlchemyModel.executor_id==user.id,
        TicketAlchemyModel.ticket_name==ticket_name,
        ))
    print(111111111111111111111111111111111111)
    try:
        result = await session.execute(check_stmt)
        print(2222222222222222222222222222)
        check_ticket = result.scalar_one_or_none()
    except JSONDecodeError as e:
        print(f"!!!!!!!!!!!!!!!!!!!JSON decode error in check_stmt: {e}")
    # result: Result = await session.execute(check_stmt)
    # check_ticket = result_1.scalar_one_or_none()
    if check_ticket:
        await add_to_existing_tickets(ticket_id=check_ticket.id,
                                      amount=ticket_in.amount,
                                      message=ticket_in.message,
                                      executor=user,
                                      session=session)

        # update_ticket = (
        #     update(TicketAlchemyModel)
        #     .where(TicketAlchemyModel.id==check_ticket.id)
        #     .values({
        #         "amount": TicketAlchemyModel.amount + ticket_in.amount, 
        #         "message": TicketAlchemyModel.message + [ticket_in.message]
        #     })
        # )
        # await session.execute(update_ticket)
        # await session.commit()
        # return await session.get(TicketAlchemyModel, check_ticket.id)

    ticket = TicketAlchemyModel(ticket_name=ticket_name,
                                message=[ticket_in.message],
                                amount=ticket_in.amount,
                                acceptor_id=acceptor.id,
                                executor_id=user.id)
    session.add(ticket)
    await session.commit()
    await session.refresh(ticket)

    return ticket


async def ticker_done(ticket_id: int, 
                      acceptor: UserWithId, 
                      session: AsyncSession) -> TicketAlchemyModel | None:
    stmt = select(TicketAlchemyModel.amount).where(TicketAlchemyModel.id==ticket_id, TicketAlchemyModel.acceptor_id==acceptor.id)
    result: Result  = await session.execute(stmt)
    ticket: int = result.scalar_one_or_none()
    if not ticket:
        return None
    elif ticket <= 1:
        await delete_ticket(ticket_id=ticket_id, session=session)
        return None
    
    ticket_done = update(TicketAlchemyModel).where(TicketAlchemyModel.id==ticket_id).values({"amount": ticket-1})
    await session.execute(ticket_done)
    await session.commit()
    refresh_ticket: TicketAlchemyModel = await session.get(TicketAlchemyModel, ticket_id)

    return refresh_ticket
    
    
async def add_to_existing_tickets(ticket_id: int,
                                  amount: int, 
                                  executor: UserWithId,
                                  message: str,
                                  session: AsyncSession) -> TicketAlchemyModel:
    
    stmt = select(TicketAlchemyModel).where(and_(TicketAlchemyModel.id==ticket_id,
                                                 TicketAlchemyModel.executor_id==executor.id))
    result: Result = await session.execute(stmt)
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ticket not found"
            )
        
    update_ticket = (update(TicketAlchemyModel)
                     .where(and_(
                        TicketAlchemyModel.id==ticket_id, 
                        TicketAlchemyModel.executor_id==executor.id))
                     .values({
                        "amount": TicketAlchemyModel.amount + amount, 
                        "message": TicketAlchemyModel.message + [message]
            })
        )
    await session.execute(update_ticket)
    await session.commit()

    return await session.get(TicketAlchemyModel, ticket_id)


async def delete_ticket(ticket_id, session):
    ticket: TicketAlchemyModel = await session.get(TicketAlchemyModel, ticket_id)
    await session.delete(ticket)
    await session.commit()
    