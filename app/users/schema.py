from typing import Optional
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    name: str
    fullname: Optional["str"]
    password: str
    age: int


class UserPatch(BaseModel):
    name: Optional["str"] = None
    fullname: Optional["str"] = None
    password: Optional["str"] = None
    age: Optional["int"] = None


class UserBase(User):
    model_config = ConfigDict(from_attributes=True)

    id: int