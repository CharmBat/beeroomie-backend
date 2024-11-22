from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from schemas.Authentication import Token, UserInDB,RegisterRequest
from services.Authentication import authenticate_user, create_access_token, get_current_user,register_user_request
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES"))


router = APIRouter()

@router.get("/users/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # Use username field as email !!!! It is workaround for not implemening email field in OAuth2PasswordRequestForm
    email = form_data.username 
    user = authenticate_user(email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(register_request: RegisterRequest):
    register_user_request(register_request.email,register_request.password)
    return {"message": "User registered successfully"}

