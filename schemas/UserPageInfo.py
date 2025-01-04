from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import date

class UserPageInfoBase(BaseModel):
    full_name: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[bool]
    smoking: Optional[bool]
    pet: Optional[bool]
    ppurl: Optional[str]
    about: Optional[str]
    contact: Optional[str]
    rh: Optional[bool]

class UserPageInfoSchema(UserPageInfoBase):
    userid_fk: Optional[int] = None
    departmentid_fk: Optional[int]
    

class UserPageInfoResponseSchema(UserPageInfoBase):
    userid_fk: int
    departmentid_fk:int
    department_name: Optional[str]  # Department adı dahil edilebilir
    
    model_config = ConfigDict(from_attributes=True)

class UserPageInfoResponse(BaseModel):
    user_info_list: Optional[list[UserPageInfoResponseSchema]] = None
    user_message: str
    error_status: int
    system_message: str
