from pydantic import BaseModel
from typing import Optional
from fastapi_mail import MessageSchema


    # Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userid: Optional[int] = None
    role: Optional[bool] = None
    
class UserMe(TokenData):
    full_name: Optional[str] = None
    rh: Optional[bool] = None # roomie 0 housie 1
    ppurl: Optional[str] = None


class UserInDB(BaseModel):
    userid: int
    e_mail: str
    role: bool
    hashed_password: str
    is_confirmed: bool
    
class RegisterRequest(BaseModel):
    email:str
    password: str


class AuthResponse(BaseModel):
    access_token: Optional[str] = None
    user_message: str
    error_status:int
    system_message: str    

class MeResponse(BaseModel):
    user: UserMe
    user_message: str
    error_status:int
    system_message: str


class EmailSchema(MessageSchema):
    subject: str
    recipient: str  # Birden fazla e-posta adresi alabilir
    body: str  # E-posta içeriği
    subtype: Optional[str] = "plain"  # Varsayılan olarak düz metin
