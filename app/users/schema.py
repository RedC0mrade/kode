from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    username: str
    password: str | bytes
    email: EmailStr

    def __str__(self):
        return f"{self.__class__.__name__} username={self.username!r}, email={self.email})"

    def __repr__(self):
        return str(self)


class UserPatch(BaseModel):
    username: Optional["str"] = None
    password: Optional["str"] = None
    email: Optional["EmailStr"] = None

    def __str__(self):
        return f"{self.__class__.__name__} username={self.username!r}, email={self.email})"

    def __repr__(self):
        return str(self)


class UserWithId(User):
    model_config = ConfigDict(from_attributes=True)

    id: int
    password: bytes

    def __str__(self):   
        return f"{self.__class__.__name__} id = {self.id}, name={self.username!r}, email={self.email}"
    
    def __repr__(self):
        return str(self)