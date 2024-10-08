from typing import Optional
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    username: str
    fullname: Optional["str"]
    password: str
    age: int
    def __str__(self):   
        return f"User(name={self.name}, fullname={self.fullname}, age={self.age})"


class UserPatch(BaseModel):
    username: Optional["str"] = None
    fullname: Optional["str"] = None
    password: Optional["str"] = None
    age: Optional["int"] = None


class UserWithId(User):
    model_config = ConfigDict(from_attributes=True)

    id: int
    def __str__(self):   
        return f"id = {self.id}, name={self.name}, fullname={self.fullname}, age={self.age}"