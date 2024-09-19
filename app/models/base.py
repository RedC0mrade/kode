from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.derective
    def __tablename__(cls) -> str:
        return f"{cls.name.lower()}s"
    
    id: Mapped[int] = mapped_column(primary_key=True)
