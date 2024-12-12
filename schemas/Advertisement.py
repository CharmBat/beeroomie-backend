from pydantic import BaseModel
from datetime import date
from typing import Optional,List





class AdPageSchema(BaseModel):
    adpageid: Optional[int]  # İsteğe bağlı hale getirildi
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
    gender_choices: int
    ad_date: date

    class Config:
        from_attributes = True


class AdPageFilter(BaseModel):      #Page filtering için, district gibi değişkenler eklenecek
    furnished: Optional[bool] = None
    max_price: Optional[int] = None
    min_price: Optional[int] = None
    pet: Optional[bool] = None
    smoking: Optional[bool] = None
    gender_choices: Optional[int] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0

class AdPageResponseSchema(BaseModel):
    adpageid: int
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
    gender_choices: int
    ad_date: date

    class Config:
        from_attributes = True


class AdPageResponse(BaseModel):
    advertisement_list: Optional[List[AdPageResponseSchema]] = None
    user_message: str
    error_status:int
    system_message: str    


'''
Top declaration works with Sqlalchemy orm
TODO: Need to use one schema. Discuss later
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
