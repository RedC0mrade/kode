from datetime import datetime, timedelta, timezone
import uuid
import jwt

from app.config import settings


def encode_token(payload: dict, 
                 private_key: str = settings.private_key.read_text(), 
                 algorithm: str = settings.algorithm,
                 expire_minutes: int = settings.access_token_expire_minute,
                 expare_time_delta: timedelta | None = None):
    
    now = datetime.now(timezone.utc)
    to_encode = payload.copy()

    if expare_time_delta:
        exp = now + expare_time_delta
    else:
        exp = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=exp, iat=now, jti=str(uuid.uuid4()))
    
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    
    return encoded


def decoded_token(token: str | bytes, 
                  public_key: str = settings.public_key.read_text(), 
                  algorithm: str = settings.algorithm):
    
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    
    return decoded