from pydantic import BaseModel

from app.users.schema import UserWithId


class Ticket(BaseModel):

    id: int
    ticket_name: str
    message: str
    amount: str
    
    acceptor: UserWithId
    acceptor_id: int

    executor: UserWithId
    executor_id: int

class CreateTicket(BaseModel):

    ticket_name: str
    message: str
    amount: int
    acceptor_username: str