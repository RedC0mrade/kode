from typing import List
from pydantic import BaseModel, ConfigDict, Field

from app.tags.schema import Tag
from app.users.schema import UserWithId


class Ticket(BaseModel):

    id: int
    ticket_name: str
    message: List[str | None]
    tags: List[Tag | None]
    amount: int
    acceptor: UserWithId
    acceptor_id: int
    executor: UserWithId
    executor_id: int

    model_config = ConfigDict(from_attributes=True)


class CreateTicket(BaseModel):

    ticket_name: str
    message: str
    amount: int = Field(..., gt=0)
    acceptor_id: int
    tags_id: list[int | None]


class UpdateTicket(BaseModel):

    ticket_name: str
    message: str
    amount: int = Field(..., gt=0)
    tags_id: list[int | None]
