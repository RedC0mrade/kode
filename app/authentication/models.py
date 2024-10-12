from pydantic import BaseModel


class Token(BaseModel):
    acceess_token: str
    token_type: str
