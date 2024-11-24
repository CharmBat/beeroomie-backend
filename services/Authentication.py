from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from utils.Authentication import verify_password,get_password_hash
from schemas.Authentication import TokenData
from schemas.Authentication import AuthResponse
from crud.Authentication import get_user, add_user_to_db
from config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES
# Temporary database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def register_user_service(email: str, password: str):
    if get_user(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = get_password_hash(password)

    add_user_to_db(email, hashed_password)

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
        userid: int = payload.get("sub")
        if userid is None:
            raise credentials_exception
        token_data = TokenData(userid=userid)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.userid)
    if user is None:
        raise credentials_exception
    return user

def login_service(email: str, password: str) -> AuthResponse:
    # Authenticate user
    user = authenticate_user(email, password)
    if not user:
        return AuthResponse(
            token=None,
            user_message="Login failed. Please check your credentials.",
            error_status=status.HTTP_401_UNAUTHORIZED,
            error_message="Incorrect email or password"
        )
    
    # Create access token with expiration
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.userid}, expires_delta=access_token_expires
    )
    
    # Return successful response
    return AuthResponse(
        token=access_token,
        user_message="Login successful",
        error_status=status.HTTP_200_OK,
        error_message=""
    )