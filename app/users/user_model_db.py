from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db_core.base import Base


class UserAlchemyModel(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"id={self.id!r}, username={self.username!r}"
    
    def __str__(self) -> str:
        return f"id={self.id}, username={self.username}"