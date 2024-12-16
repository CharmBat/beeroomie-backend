from fastapi import Depends,APIRouter
from schemas.Authentication import AuthResponse, UserInDB,RegisterRequest,LoginRequest
from services.Authentication import login_service, get_current_user,register_user_service, confirm_user_service, delete_user_service, logout_service, change_password_service,forgot_password_service

router = APIRouter(tags=["Authentication"])

@router.get("/users/me", response_model=UserInDB)
async def read_user_data(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@router.post("/auth/login", response_model=AuthResponse)
async def login(form_data: LoginRequest):
    return login_service(form_data.email, form_data.password)

@router.post("/auth/register", response_model=AuthResponse)
async def register_user(register_request: RegisterRequest):
    return register_user_service(register_request.email,register_request.password)

@router.get("/auth/confirm/{token}", response_model=AuthResponse)
async def confirm_user(token: str):
    return confirm_user_service(token)

@router.delete("/auth/delete/{token}")
async def delete_user(token: str):
    return delete_user_service(token)


@router.get("/auth/change-password/{token}")
async def change_password(token: str, new_password: str):
    return change_password_service(token, new_password)

@router.post("/auth/logout/{token}", response_model=AuthResponse)
async def logout(token: str):
    return logout_service(token)

@router.post("/auth/forgot-password/", response_model=AuthResponse)
async def forgot_password(email: str):
    return forgot_password_service(email)