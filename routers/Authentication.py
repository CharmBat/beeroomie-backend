from fastapi import Depends,APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from schemas.Authentication import Token, UserInDB,RegisterRequest,RegisterResponse
from services.Authentication import login_service, get_current_user,register_user_service



router = APIRouter()

@router.get("/users/me", response_model=UserInDB)
async def read_user_data(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@router.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Use username field as email (workaround for not implementing email field in OAuth2PasswordRequestForm)
    email = form_data.username 
    password=form_data.password
    access_token=login_service(email, password)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/register")
async def register_user(register_request: RegisterRequest):
    register_user_service(register_request.email,register_request.password)
    return {"message": "User registered successfully"}

