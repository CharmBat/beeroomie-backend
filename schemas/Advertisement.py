from pydantic import BaseModel
from datetime import date
from typing import Optional,List,Union

    

class AdPageBase(BaseModel):
    adpageid: Optional[int]  # Bu basede mi adpageschema da mı olmalı idk
    title: str
    price: int
    adtype: bool
    m2: int
    n_floor: int
    floornumber: int
    pet: bool
    smoking: bool
    furnished: bool
    description: str
    address: str
    ad_date: date

class AdPageSchema(AdPageBase):
    userid_fk: int
    neighborhoodid_fk: int
    n_roomid_fk: int
    gender_choices: int
    class Config:
        from_attributes = True

class AdPageRequest(AdPageSchema):
    photos: list[str]
    utilites:List[int]
    


class AdPageResponseSchema(AdPageBase):
    user_full_name: str
    neighborhood: str
    district: str
    n_room: str
    gender_choices: str
    photos: list[str]
    utilities:List[str]

    class Config:
        from_attributes = True

class AdListingResponseSchema(BaseModel):
    adpageid: int
    title: str
    address: str
    pet: bool
    smoking: bool
    price: int
    adtype: bool
    full_name: str
    photos: list[str]



class AdPageResponse(BaseModel):
    advertisement_list: Optional[List[Union[AdPageResponseSchema, AdListingResponseSchema]]] = None
    user_message: str
    error_status:int
    system_message: str    



'''
Top declaration works with Sqlalchemy orm
TODO: Need to use one schema. Discuss later
'''
