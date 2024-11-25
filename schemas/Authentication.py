from pydantic import BaseModel
from fastapi import HTTPException
from typing import List, Optional
from fastapi_mail import MessageSchema


    # Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userid: Optional[int] = None

class UserBase(BaseModel):
    userid: int
    e_mail: str

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


class EmailSchema(MessageSchema):
    subject: str
    recipient: str  # Birden fazla e-posta adresi alabilir
    body: str  # E-posta içeriği
    subtype: Optional[str] = "plain"  # Varsayılan olarak düz metin
