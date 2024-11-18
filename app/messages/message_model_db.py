from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_core.base import Base


if TYPE_CHECKING:
    from app.tickets.ticket_model_db import TicketAlchemyModel


class MessageAlchemyModel(Base):
    __tablename__ = "messages"

    message: Mapped[str] = mapped_column(String(250), nullable=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    ticket: Mapped["TicketAlchemyModel"] = relationship("TicketAlchemyModel", 
                                                        back_populates="messages")