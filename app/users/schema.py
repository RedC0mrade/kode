from typing import Optional
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    """Модель пользователя"""
    name: str
    fullname: Optional["str"]
    password: str
    age: int


class UserCreate(User):
    pass


class UserPut(User):
    pass


class UserPatch(User):
    name: Optional["str"] = None
    fullname: Optional["str"] = None
    password: Optional["str"] = None
    age: Optional["int"] = None


class UserBase(User):
    model_config = ConfigDict(from_attributes=True)

    id: int