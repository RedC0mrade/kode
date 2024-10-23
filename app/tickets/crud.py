from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from app.users.schema import UserWithId
from app.users.user_model_db import UserAlchemyModel
from app.tickets.schema import CreateTicket, Ticket


async def create_ticket(ticket_in: CreateTicket,
                        user: UserWithId,
                        session: AsyncSession) -> Ticket:
    stmt = select(UserAlchemyModel).where(UserAlchemyModel.usename==ticket_in.acceptor_username)
    result: Result = await session.execute(stmt)
    acceptor = result.scalar_one_or_none(result)
    ticket = Ticket(ticket_name=ticket_in.ticket_name,
                    message=ticket_in.message,
                    amount=ticket_in.amount,
                    acceptor=acceptor,
                    executor=user,
                    executor_id=user.id)
    session.add(ticket)
    await session.commit()
    return ticket