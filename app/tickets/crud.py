from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from app.users.schema import UserWithId
from app.users.user_model_db import UserAlchemyModel
from app.tickets.schema import CreateTicket, Ticket
from app.tickets.ticket_model_db import TicketAlchemyModel


async def create_ticket(ticket_in: CreateTicket,
                        user: UserWithId,
                        session: AsyncSession) -> None:
    stmt = select(UserAlchemyModel).where(UserAlchemyModel.username==ticket_in.acceptor_username)
    result: Result = await session.execute(stmt)
    print("0------------------------------------")
    acceptor = result.scalar_one_or_none()
    print(acceptor.id)
    print("1------------------------------------")
    print(user)
    print("2------------------------------------")

    ticket = TicketAlchemyModel(ticket_name=ticket_in.ticket_name,
                                message=ticket_in.message,
                                amount=ticket_in.amount,
                                acceptor_id=acceptor.id,
                                # acceptor=acceptor,
                                # executor=user,
                                executor_id=user.id)
    print(ticket)
    session.add(ticket)
    await session.commit()
    print(ticket)
    return None 


async def delete_ticket(ticket_id, session):
    ticket: TicketAlchemyModel = await session.get(TicketAlchemyModel, ticket_id)
    await session.delete(ticket)
    await session.commit()
    