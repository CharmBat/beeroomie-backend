from pydantic import BaseModel
from typing import Optional

    # Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str
    userId: str

class UserInDB(UserBase):
    hashed_password: str

class RegisterRequest(BaseModel):
    full_name: str
    email:str
    password: str
