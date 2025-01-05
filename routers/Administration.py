from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.Administration import ReportRequest, ReportResponse, BlacklistResponse
from services.Administration import AdministrationService
from services.Authentication import AuthenticationService
from schemas.Authentication import TokenData

router = APIRouter(prefix="/administration", tags=["Administration"])


@router.post("/report", response_model=ReportResponse)
async def create_report(report_data: ReportRequest, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdministrationService.report_user_service(report_data, db, user_id=current_user.userid)
    else:
        return current_user

@router.delete("/report/{report_id}", response_model=ReportResponse)
def delete_report(report_id: int, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdministrationService.delete_report_service(report_id, db, user_id=current_user.userid, user_role=current_user.role)
    else:
        return current_user


@router.get("/report", response_model=ReportResponse)
def get_reports(db: Session =Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdministrationService.get_all_reports(db, role=current_user.role)
    else:
        return current_user


@router.delete("/ban/{user_id}", response_model=ReportResponse)
def ban_user(user_id: int, ban_reason: str, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdministrationService.ban_user_service(role=current_user.role, user_id=user_id, ban_reason=ban_reason, db=db)
    else:
        return current_user
    
@router.get("/blacklist", response_model=BlacklistResponse)
def get_blacklist(db: Session =Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return AdministrationService.get_blacklist(db)
    else:
        return current_user
