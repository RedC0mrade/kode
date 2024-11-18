from sqlalchemy import JSON, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from app.db_core.base import Base

if TYPE_CHECKING:
    from app.users.user_model_db import UserAlchemyModel
    from app.tags.tag_model_db import TagAlchemyModel
    from app.messages.message_model_db import MessageAlchemyModel

class TicketAlchemyModel(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        UniqueConstraint("acceptor_id", "executor_id", "ticket_name", name="unique_ticket"),
    )

    ticket_name: Mapped[str] = mapped_column(String(100))
    messages: Mapped[List["MessageAlchemyModel"]] = relationship("MessageAlchemyModel",
                                                                 back_populates="ticket",
                                                                 cascade="all, delete-orphan",
                                                                 lazy="selectin")
    amount: Mapped[int] = mapped_column(Integer)

    executor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    executor: Mapped["UserAlchemyModel"] = relationship("UserAlchemyModel", 
                                                        foreign_keys=[executor_id], 
                                                        back_populates="to_do_tickets",
                                                        lazy="joined")

    acceptor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    acceptor: Mapped["UserAlchemyModel"] = relationship("UserAlchemyModel", 
                                                        foreign_keys=[acceptor_id], 
                                                        back_populates="to_take_tickets",
                                                        lazy="joined")
    
    tags: Mapped[list["TagAlchemyModel"]] = relationship(secondary="ticket_tag",
                                                       back_populates="tickets",
                                                       lazy="selectin")
    def __str__(self) -> str:
        return f"id={self.id}, ticket_name={self.ticket_name}"
    