from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.db_core.base import Base


from app.tickets.ticket_model_db import TicketAlchemyModel


class UserAlchemyModel(Base):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    to_do_tickets: Mapped[list["TicketAlchemyModel"]] = relationship(
        "TicketAlchemyModel",
        foreign_keys="[TicketAlchemyModel.executor_id]",
        back_populates="executor", 
        cascade="all, delete-orphan"
        )

    to_take_tickets: Mapped[list["TicketAlchemyModel"]] = relationship(
        "TicketAlchemyModel",
        foreign_keys="[TicketAlchemyModel.acceptor_id]",
        back_populates="acceptor", 
        cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"id={self.id!r}, username={self.username!r}"
    
    def __str__(self) -> str:
        return f"id={self.id}, username={self.username}"