from pydantic import BaseModel, ConfigDict

from app.users.schema import UserWithId


class Ticket(BaseModel):

    id: int
    ticket_name: str
    message: str
    amount: int
    acceptor: UserWithId
    acceptor_id: int
    executor: UserWithId
    executor_id: int

    model_config = ConfigDict(from_attributes=True)

class CreateTicket(BaseModel):

    ticket_name: str
    message: str
    amount: int
    acceptor_username: str