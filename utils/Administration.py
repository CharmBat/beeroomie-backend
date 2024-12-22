from sqlalchemy.orm import Session
from typing import List
from schemas.Administration import BlacklistResponse, ReportResponse, BlacklistBase, ReportResponseSchema
from models.Administration import Blacklist, Reports

def create_response_blacklist(user_message: str, error_status: int, system_message: str, blacklist_list: List[BlacklistBase] = None):
    return BlacklistResponse(
        blacklist_list=blacklist_list,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )

def create_response_reports(user_message: str, error_status: int, system_message: str, report_list: List[ReportResponseSchema] = None):
    return ReportResponse(
        report_list=report_list,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )
