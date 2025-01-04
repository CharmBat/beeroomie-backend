from fastapi import Depends,APIRouter
from db.database import get_db
from schemas.Authentication import AuthResponse,RegisterRequest,TokenData,MeResponse
from services.Authentication import AuthenticationService
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated
from services.UserPageInfo import UserPageInfoService

router = APIRouter(tags=["Authentication"])

@router.get("/users/me", response_model=MeResponse)
async def read_user_data(current_user: TokenData = Depends(AuthenticationService.get_current_user), db: Session = Depends(get_db)):
    if isinstance(current_user, TokenData):
        return UserPageInfoService.current_user_service(current_user.userid,current_user.role,db)
    else:
        return current_user
@router.post("/auth/login", response_model=AuthResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return AuthenticationService.login_service(form_data.username, form_data.password,db)

@router.post("/auth/register", response_model=AuthResponse)
async def register_user(register_request: RegisterRequest, db: Session = Depends(get_db)):
    return AuthenticationService.register_user_service(register_request.email,register_request.password,db)

@router.get("/auth/confirm/{token}", response_model=AuthResponse)
async def confirm_user(token: str, db: Session = Depends(get_db)):
    return AuthenticationService.confirm_user_service(token,db)

# Buna endpoint olarak gerek yok çünkü bunu userpageden çağırıyoruz
# @router.delete("/auth/delete/", response_model=AuthResponse)
# async def delete_user(db: Session = Depends(get_db),current_user = Depends(AuthenticationService.get_current_user)):
#     if isinstance(current_user, TokenData):
#         return AuthenticationService.delete_user_service(userid=current_user.userid,db=db)
#     else:
#         current_user

@router.get("/auth/change-password/{token}")
async def change_password(token: str, new_password: str, db: Session = Depends(get_db)):
    return AuthenticationService.change_password_service(token, new_password,db)

@router.post("/auth/logout/{token}", response_model=AuthResponse)
async def logout(token: str):
    return AuthenticationService.logout_service(token)

@router.post("/auth/forgot-password/", response_model=AuthResponse)
async def forgot_password(email: str, db: Session = Depends(get_db)):
    return AuthenticationService.forgot_password_service(email,db)