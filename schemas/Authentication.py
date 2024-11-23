from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException


    # Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userID: Optional[str] = None

class UserBase(BaseModel):
    email: str
    userId: str

class UserInDB(UserBase):
    hashed_password: str

class RegisterRequest(BaseModel):
    full_name: str
    email:str
    password: str

class LoginRequest(BaseModel):
    email:str
    password: str    

class AuthResponse(BaseModel):
    token: Optional[str] = None
    user_message: str
    error_status:int
    error_message: str    
