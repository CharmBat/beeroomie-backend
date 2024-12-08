from pydantic import BaseModel
from datetime import date
from typing import Optional,List


class AdPageSchema(BaseModel):
    adpageID: int
    userid_fk: int
    neighborhoodid_fk: int
    n_roomid_fk: int
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
    gender_choice: int
    ad_date: date

    class Config:
        orm_mode = True

class AdPageResponseSchema(BaseModel):
    adpageID: int
    userid_fk: int
    neighborhoodid_fk: int
    n_roomid_fk: int
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
    gender_choice: int
    ad_date: date

    class Config:
        orm_mode = True


'''
Top declaration works with Sqlalchemy orm
TODO: Need to use one schema.
'''

class AdvertisementBase(BaseModel):
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
    gender_choice: int

class AdvertisementInDB(AdvertisementBase):
    neighborhoodID: int
    districtID: int
    n_roomID: int
    photos: list[dict]#dict -> {photo1: "url", photo2: "url", photo3: "url"}

class AdvertisementFrontEnd(AdvertisementBase):
    neighborhood: str #fetched from neighborhoodID lookup
    district: str #fetched from districtID lookup
    n_room: int #fetched from n_roomID lookup
    photos: list[dict]#dict -> {photo1: "url", photo2: "url", photo3: "url"}




class AdvertisementResponse(BaseModel):
    advertisement_list: Optional[List[AdvertisementFrontEnd]] = None
    user_message: str
    error_status:int
    system_message: str    
