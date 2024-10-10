import bcrypt
import jwt

from config import settings

def encode_token(payload: dict, 
                 private_key: str = settings.private_key.read_text(), 
                 algorithm: str = settings.algorithm):
    
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    
    return encoded

def decoded_token(token: str | bytes, 
                  public_key: str = settings.public_key.read.text(), 
                  algorithm: str = settings.algorithm):
    
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    
    return decoded

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)