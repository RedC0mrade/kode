from app.authentication.token_utils import decoded_token, encode_token

# from app.db_core.config import settings
from app.db_core.engine import db_helper

print(type(db_helper))
play = {"username": "NNN",
        "password": "123",
        "email": "qwerty@mail.ru"}

# n = encode_token(play)

# print(n)