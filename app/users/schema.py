from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    username: str
    password: str | bytes
    email: EmailStr
    def __str__(self):   
        return f"User(name={self.username}, email={self.email})"


class UserPatch(BaseModel):
    username: Optional["str"] = None
    password: Optional["str"] = None
    email: Optional["EmailStr"] = None


class UserWithId(User):
    model_config = ConfigDict(from_attributes=True)

    id: int
    password: bytes
    def __str__(self):   
        return f"id = {self.id}, name={self.username}, email={self.email}"