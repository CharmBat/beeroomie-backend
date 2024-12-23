from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.Administration import ReportRequest, ReportResponse
from services.Administration import AdministrationService
from services.Authentication import AuthenticationService
from schemas.Authentication import TokenData

router = APIRouter(prefix="/administration", tags=["Administration"])


@router.post("/report", response_model=ReportResponse)
async def create_report(report_data: ReportRequest, db: Session = Depends(get_db), current_user: TokenData = Depends(AuthenticationService.get_current_user)):
    return AdministrationService.report_user_service(report_data, db, current_user)


@router.delete("/report/{report_id}", response_model=ReportResponse)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    return AdministrationService.delete_report_service(report_id, db)


@router.get("/report", response_model=ReportResponse)
def get_reports(db: Session =Depends(get_db)):
    return AdministrationService.get_all_reports(db)

@router.delete("/administration/ban/{user_id}", response_model=dict)
def ban_user(user_id: int, ban_reason: str, db: Session = Depends(get_db), current_user: TokenData = Depends(AuthenticationService.get_current_user)):
    return AdministrationService.ban_user_service(token=current_user, user_id=user_id, ban_reason=ban_reason, db=db)
