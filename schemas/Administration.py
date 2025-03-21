from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import date
from pydantic import ConfigDict

# Blacklist Schemas
class BlacklistBase(BaseModel):
    e_mail: str
    ban_date: date
    ban_reason: str

class BlacklistResponse(BaseModel):
    blacklist_list: Optional[List[BlacklistBase]] = None
    user_message: str
    error_status: int
    system_message: str

    model_config = ConfigDict(from_attributes=True)


# Report Schemas
class ReportBase(BaseModel):
    #reporter: int
    reportee: int
    description: str
    report_date: date

class ReportRequest(BaseModel):
    #reporter: int
    reportee: int
    description: str


class ReportResponseSchema2(BaseModel):
    report_id: Optional[int]
    reporter: int
    reportee: int
    description: str
    report_date: date

    model_config = ConfigDict(from_attributes=True)

class ReportResponseSchema(BaseModel):
    report_id: int
    reporter_id: int
    reportee_id: int
    reporter: str
    reportee: str
    description: str
    report_date: date

    model_config = ConfigDict(from_attributes=True)

class ReportResponse(BaseModel):
    report_list: Optional[List[Union[ReportResponseSchema, ReportResponseSchema2]]] = None
    user_message: str
    error_status: int
    system_message: str

    model_config = ConfigDict(from_attributes=True)
