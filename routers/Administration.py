from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.Administration import ReportRequest, ReportResponse
from services.Administration import AdministrationService
from db.database import get_db

router = APIRouter(prefix="/administration", tags=["Administration"])

@router.post("/report", response_model=ReportResponse)
def report_user(report_data: ReportRequest, db: Session = Depends(get_db)):
    return AdministrationService.report_user_service(report_data, db)


@router.delete("/report/{report_id}", response_model=ReportResponse)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    return AdministrationService.delete_report_service(report_id, db)
