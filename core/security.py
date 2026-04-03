import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(plaintext_password:str, hashed_password:str):
    return pwd_context.verify(plaintext_password, hashed_password)

def create_token(data: dict):
    datacopy_to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN)
    datacopy_to_encode.update({"exp": expire})
    return jwt.encode(datacopy_to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ACCESS_TOKEN])
        return payload
    except JWTError:
        return None