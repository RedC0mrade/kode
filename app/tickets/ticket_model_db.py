from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.db_core.base import Base

if TYPE_CHECKING:
    from app.users.user_model_db import UserAlchemyModel


class TicketAlchemyModel(Base):
    __tablename__ = "tickets"

    ticket_name: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(String(200))
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
