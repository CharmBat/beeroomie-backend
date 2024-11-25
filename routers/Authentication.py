from fastapi import Depends,APIRouter
from schemas.Authentication import AuthResponse, UserInDB,RegisterRequest,LoginRequest
from services.Authentication import login_service, get_current_user,register_user_service


router = APIRouter()

@router.get("/users/me", response_model=UserInDB)
async def read_user_data(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@router.post("/auth/login", response_model=AuthResponse)
async def login(form_data: LoginRequest):
    return login_service(form_data.email, form_data.password)


@router.post("/auth/register", response_model=AuthResponse)
async def register_user(register_request: RegisterRequest):
    return register_user_service(register_request.email,register_request.password)
     

