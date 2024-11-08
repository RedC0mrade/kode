import re
from sqlalchemy import String, hex
from sqlalchemy.orm import Mapped, mapped_column

from app.db_core.base import Base
from app.constant import HEX_COLOR_REGEX

class Tag(Base):
    __tablename__ = 'tag'

    tag_name: Mapped[str] = mapped_column(String(30))
    tag_color: Mapped[str] = mapped_column(String(7), nullable=False)

    def __init__(self, tag_color: str):
        if not re.match(HEX_COLOR_REGEX, tag_color):
            raise ValueError(f'invalid color format {tag_color}')
        self.tag_color = tag_color
     