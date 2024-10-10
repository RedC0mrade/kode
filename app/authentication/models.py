from pydantic import BaseModel, ConfigDict, EmailStr


class UserJwt(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
