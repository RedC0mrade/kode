from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    """Модель пользователя"""
    name: str
    fullname: str | None = None
    password: str
    age: int


class UserCreate(User):
    pass


class UserBase(User):
    model_config = ConfigDict(from_attributes=True)

    id: int