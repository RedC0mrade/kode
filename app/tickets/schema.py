from typing import Annotated, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.tags.schema import Tag
from app.users.schema import UserWithId
from app.messages.schema import Message


PositiveInt = Annotated[int, Field(gt=0)]

class Ticket(BaseModel):

    id: int
    ticket_name: str
    messages: Optional[List[Message]] = None
    tags: List[Tag]
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
    acceptor_id: PositiveInt
    tags_id: list[PositiveInt]


class UpdateTicket(BaseModel):

    message: str | None = None
    amount: PositiveInt | None = None
    tags_id: list[PositiveInt] | None = None
