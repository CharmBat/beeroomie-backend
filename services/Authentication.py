from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from utils.Authentication import get_user, verify_password,get_password_hash
from schemas.Authentication import TokenData
from dotenv import load_dotenv
import os

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")


# Temporary database
tempDatabase = {
    "gunyel20@itu.edu.tr": {
        "userId": "1",
        "email": "gunyel20@itu.edu.tr",
        "hashed_password": "$2b$12$b1SNnAwbSrjVzFf7D2d9M.izdyr1EY7tSIoWgSyHiiWJdeZbAptpO"
    }
}
db = tempDatabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def authenticate_user(email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def register_user_request(email: str, password: str):
    if get_user(db, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = get_password_hash(password)
    db[email] = {
        "email": email,
        "hashed_password": hashed_password,
    }

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user

