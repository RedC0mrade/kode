from typing import List
from sqlalchemy import and_, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.tags.schema import Tag
from app.users.schema import UserWithId
from app.tags.tag_model_db import TagAlchemyModel, TicketTagAssociation
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
                        session: AsyncSession):
    check_stmt = select(TicketAlchemyModel).where(and_(
        TicketAlchemyModel.ticket_name==ticket_in.ticket_name,
        TicketAlchemyModel.acceptor_id==ticket_in.acceptor_id,
        TicketAlchemyModel.executor_id==user.id,
        ))

    result: Result = await session.execute(check_stmt)
    check_ticket: TicketAlchemyModel = result.scalar_one_or_none()
    
    if check_ticket:
        print(check_ticket)
        # return await add_to_existing_tickets(ticket=check_ticket,
        #                                      ticket_in=ticket_in,
        #                                      session=session)

    ticket = TicketAlchemyModel(ticket_name=ticket_in.ticket_name,
                                message=[ticket_in.message],
                                amount=ticket_in.amount,
                                acceptor_id=ticket_in.acceptor_id,
                                executor_id=user.id)
    session.add(ticket)
    await session.flush()

    stmt = select(TagAlchemyModel).where(TagAlchemyModel.id.in_(ticket_in.tags_id))
    result: Result = await session.execute(stmt)
    tags: List[TagAlchemyModel] = result.scalars().all()
    associations = [TicketTagAssociation(ticket_id=ticket.id, tag_id=tag.id) for tag in tags]

    session.add_all(associations)
    await session.commit()
    await session.refresh(ticket)
    stmt = select(TicketAlchemyModel).options(
        selectinload(TicketAlchemyModel.tags)
        ).where(TicketAlchemyModel.id == ticket.id)
    result: Result = await session.execute(stmt)
 
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
                                  ticket_in: CreateTicket,
                                  session: AsyncSession) -> TicketAlchemyModel:
    
    ticket.message.append(ticket_in.message)
    update_amount: int = ticket.amount + ticket_in.amount

    update_ticket = (update(TicketAlchemyModel)
                     .where(TicketAlchemyModel.id==ticket.id)
                     .values({
                        "amount": update_amount, 
                        "message": ticket.message
            })
        )
    await session.execute(update_ticket)
    await session.commit()
    await session.refresh()
    # return await session.get(TicketAlchemyModel, ticket_id)


async def delete_ticket(ticket_id: int, session: AsyncSession) -> None:
    ticket: TicketAlchemyModel = await session.get(TicketAlchemyModel, ticket_id)
    await session.delete(ticket)
    await session.commit()


async def get_ticket(ticket_id: int, session: AsyncSession) -> TicketAlchemyModel:
    ticket: TicketAlchemyModel = await session.get(TicketAlchemyModel, ticket_id)

    return ticket
