from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (DeclarativeBase, declared_attr, Mapped, 
                            mapped_column, relationship)


class Base(DeclarativeBase):
    
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
    
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    password: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r},)"

