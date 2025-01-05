from pydantic import BaseModel,ConfigDict
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
    gender_choices: int
    ad_date: date

class AdPageSchema(AdPageBase):
    userid_fk: int
    neighborhoodid_fk: int
    n_roomid_fk: int
    
    model_config = ConfigDict(from_attributes=True)

class AdPageRequest(AdPageSchema):
    photos: list[str]
    utilites:List[int]


class AdPageFilterSchema(BaseModel):
    furnished: Optional[bool] = None
    pet: Optional[bool] = None
    smoking: Optional[bool] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    neighborhood: Optional[int] = None
    district: Optional[int] = None
    number_of_rooms: Optional[int] = None
    gender_choices: Optional[int] = None
    
class AdPageResponseSchema(AdPageBase):
    userid_fk: int
    user_full_name: str
    neighborhood: str
    district: str
    n_room: str
    photos: list[str]
    utilities:List[str]
    districtid_fk: int
    ppurl: str

    model_config = ConfigDict(from_attributes=True)

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








class UtilityResponseSchema(BaseModel):
    utilityid: int
    utility_name: str

class UtilityListResponse(BaseModel):
    user_message: str
    system_message: str
    utilities: List[UtilityResponseSchema] 




class DepartmentResponseSchema(BaseModel):
    departmentid: int
    department_name: str

class DepartmentListResponse(BaseModel):
    user_message: str
    system_message: str
    departments: List[DepartmentResponseSchema]


class NeighborhoodResponseSchema(BaseModel):
    neighborhoodid: int
    neighborhood_name: str

class NeighborhoodListResponse(BaseModel):
    user_message: str
    system_message: str
    neighborhoods: List[NeighborhoodResponseSchema]



class DistrictResponseSchema(BaseModel):
    districtid: int
    district_name: str

class DistrictListResponse(BaseModel):
    user_message: str
    system_message: str
    districts: List[DistrictResponseSchema]


class NumberOfRoomResponseSchema(BaseModel):
    n_roomid: int
    n_room: str

class NumberOfRoomListResponse(BaseModel):
    user_message: str
    system_message: str
    rooms: List[NumberOfRoomResponseSchema]