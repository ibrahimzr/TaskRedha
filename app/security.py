from datetime import datetime,timedelta,timezone
import jwt
import random
from pwdlib import PasswordHash
from app.config import settings

password_hash=PasswordHash.recommended()
DUMMY_HASH=password_hash.hash("dummy-password-for-timing")

def hash_password(password:str):
    return password_hash.hash(password)

def verify_password(password:str,hashed_password:str):
    return password_hash.verify(password,hashed_password)

def create_access_token(user_id:int):
    expires_at=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    payload={"sub":str(user_id),"exp":expires_at}
    return jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)

def read_user_id_from_token(token:str):
    try:
        payload=jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"require":["exp","sub"]},
        )
        return int(payload["sub"])
    except (jwt.InvalidTokenError,ValueError):
        return None


def create_number_challenge():
    numbers=random.sample(range(1,100),5)
    answer=",".join(str(n) for n in sorted(numbers))
    expires_at=datetime.now(timezone.utc)+timedelta(minutes=5)
    payload={"type":"number_challenge","answer":answer,"exp":expires_at}
    token=jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return numbers,token

def verify_number_challenge(token:str,answer:str):
    try:
        payload=jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        if payload.get("type")!="number_challenge":
            return False
        clean=",".join(part.strip() for part in answer.split(","))
        return clean==payload.get("answer")
    except jwt.InvalidTokenError:
        return False
