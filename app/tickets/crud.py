from typing import List
from sqlalchemy import and_, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.messages.crud import delete_all_messages
from app.users.schema import UserWithId
from app.tags.tag_model_db import TicketTagAssociation
from app.messages.crud import add_message
from app.tickets.schema import CreateTicket, UpdateTicket
from app.tickets.ticket_model_db import TicketAlchemyModel
from app.validators.tags import validate_tags_in_base
from app.validators.tickets import validate_ticket


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
    if user.id == ticket_in.acceptor_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You can't create ticket to your self")
    
    check_stmt = select(TicketAlchemyModel).where(and_(
        TicketAlchemyModel.ticket_name==ticket_in.ticket_name,
        TicketAlchemyModel.acceptor_id==ticket_in.acceptor_id,
        TicketAlchemyModel.executor_id==user.id,
        ))
    result: Result = await session.execute(check_stmt)
    check_ticket: TicketAlchemyModel = result.scalar_one_or_none()

    if check_ticket:
        return await add_to_existing_tickets(ticket=check_ticket,
                                             user=user,
                                             ticket_in=ticket_in,
                                             session=session)

    ticket = TicketAlchemyModel(ticket_name=ticket_in.ticket_name,
                                amount=ticket_in.amount,
                                acceptor_id=ticket_in.acceptor_id,
                                executor_id=user.id)
    session.add(ticket)
    await session.flush()

    await add_message(message=ticket_in.message, user=user, ticket_id=ticket.id, session=session)


    if ticket_in.tags_id:
        await validate_tags_in_base(tags=ticket_in.tags_id, session=session)
        associations = [TicketTagAssociation(ticket_id=ticket.id, tag_id=tag) for tag in ticket_in.tags_id]
        session.add_all(associations)

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
    
    
async def add_to_existing_tickets(ticket: TicketAlchemyModel,
                                  user: UserWithId,
                                  ticket_in: CreateTicket,
                                  session: AsyncSession) -> TicketAlchemyModel:
    
    add_message(message=ticket_in.message, user=user, ticket_id=ticket.id, session=session)
    
    ticket.amount += ticket_in.amount

    
    stmt = select(TicketTagAssociation.tag_id).where(TicketTagAssociation.ticket_id==ticket.id)
    result: Result = await session.execute(stmt)
    current_tags_ids = set(result.scalars().all())

    if ticket_in.tags_id:
        await validate_tags_in_base(tags=ticket_in.tags_id, session=session)
        new_tags_ids = set(ticket_in.tags_id) - current_tags_ids
        new_tags = [TicketTagAssociation(ticket_id=ticket.id, tag_id=tag) for tag in new_tags_ids]
        session.add_all(new_tags)

    await session.commit()
    await session.refresh(ticket)
    return ticket


async def delete_ticket(ticket_id: int,
                        user: UserWithId,
                        session: AsyncSession) -> None:
    ticket: TicketAlchemyModel = validate_ticket(ticket_id=ticket_id, user=user, session=session)
    await session.delete(ticket)
    await session.commit()


async def get_ticket(ticket_id: int,
                     user: UserWithId,
                     session: AsyncSession) -> TicketAlchemyModel:
    ticket: TicketAlchemyModel = validate_ticket(ticket_id=ticket_id, user=user, session=session)
    return ticket


async def update_ticket(ticket_id: int, 
                        ticket_in: UpdateTicket,
                        executor: UserWithId, 
                        session: AsyncSession) -> TicketAlchemyModel:
    
    ticket: TicketAlchemyModel = await validate_ticket(ticket_id=ticket_id, user=executor, session=session)
    
    if ticket_in.message:
        await delete_all_messages(ticket_id=ticket_id, user=executor, session=session)

        await add_message(ticket_id=ticket_id,
                          message=ticket_in.message,
                          user=executor,
                          session=session)
        
    if ticket_in.amount and ticket_in.amount > ticket.amount:
        ticket.amount = ticket_in.amount

    if ticket_in.tags_id:
        