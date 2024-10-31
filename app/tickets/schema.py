from enum import Enum
from typing import List
from pydantic import BaseModel, ConfigDict, Field

from app.users.schema import UserWithId


class TicketName(str, Enum):
    wash = "wash"
    clean = "clean"
    garbage = "garbage"
    vacuum = "vacuum"
    iron = "iron"

class Ticket(BaseModel):

    id: int
    ticket_name: TicketName
    message: List[str]
    amount: int
    acceptor: UserWithId
    acceptor_id: int
    executor: UserWithId
    executor_id: int

    model_config = ConfigDict(from_attributes=True)

class CreateTicket(BaseModel):

    ticket_name: TicketName
    message: str
    amount: int = Field(..., gt=0)
    acceptor_username: str
