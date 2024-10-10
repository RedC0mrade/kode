from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db_core.base import Base


class UserAlchemyModel(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"id={self.id!r}, name={self.username!r}, fullname={self.fullname!r}, password={self.password!r}"
    
    def __str__(self) -> str:
        return (f"User(id={self.id}, name={self.username}, fullname={self.fullname}, password={self.password})")