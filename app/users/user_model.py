from pydantic import BaseModel


class UserBase(BaseModel):
    """Base user model"""
    id: int


class User(UserBase):
    """User model"""
    user_name: str
    password: str
    age: int