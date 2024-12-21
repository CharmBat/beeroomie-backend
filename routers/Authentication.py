from fastapi import Depends,APIRouter
from db.database import get_db
from schemas.Authentication import AuthResponse, UserInDB,RegisterRequest,LoginRequest
from services.Authentication import AuthenticationService
from sqlalchemy.orm import Session

router = APIRouter(tags=["Authentication"])

@router.get("/users/me", response_model=UserInDB)
async def read_user_data(current_user: UserInDB = Depends(AuthenticationService.get_current_user)):
    return current_user

@router.post("/auth/login", response_model=AuthResponse)
async def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    return AuthenticationService.login_service(form_data.email, form_data.password,db)

@router.post("/auth/register", response_model=AuthResponse)
async def register_user(register_request: RegisterRequest, db: Session = Depends(get_db)):
    return AuthenticationService.register_user_service(register_request.email,register_request.password,db)

@router.get("/auth/confirm/{token}", response_model=AuthResponse)
async def confirm_user(token: str, db: Session = Depends(get_db)):
    return AuthenticationService.confirm_user_service(token,db)

@router.delete("/auth/delete/{token}", response_model=AuthResponse)
async def delete_user(token: str, db: Session = Depends(get_db)):
    return AuthenticationService.delete_user_service(token,db)


@router.get("/auth/change-password/{token}")
async def change_password(token: str, new_password: str, db: Session = Depends(get_db)):
    return AuthenticationService.change_password_service(token, new_password,db)

@router.post("/auth/logout/{token}", response_model=AuthResponse)
async def logout(token: str):
    return AuthenticationService.logout_service(token)

@router.post("/auth/forgot-password/", response_model=AuthResponse)
async def forgot_password(email: str, db: Session = Depends(get_db)):
    return AuthenticationService.forgot_password_service(email,db)