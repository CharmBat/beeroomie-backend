from sqlalchemy.orm import Session
from datetime import date
from models.Administration import Blacklist, Reports
from schemas.Administration import BlacklistBase, BlacklistResponse, ReportBase, ReportRequest, ReportResponseSchema, ReportResponse
from crud.Authentication import AuthCRUD
from datetime import datetime
from schemas.Administration import (
    BlacklistBase,
    BlacklistResponse,
    ReportRequest,
    ReportResponseSchema,
    ReportResponse
)

class BlacklistCRUD:
    @staticmethod
    def get_blacklist_by_user(db: Session, user_id: int) -> BlacklistResponse:
        blacklist_entries = (
            db.query(Blacklist)
            .filter(Blacklist.userid_fk == user_id)
            .all()
        )
        response_data = [
            BlacklistBase(
                userid_fk=entry.userid_fk,
                ban_date=entry.ban_date,
                ban_reason=entry.ban_reason
            )
            for entry in blacklist_entries
        ]
        return BlacklistResponse(
            blacklist_list=response_data,
            user_message="Blacklist data retrieved successfully",
            error_status=0,
            system_message="Operation completed"
        )

    @staticmethod
    def create_blacklist(db: Session, blacklist_data: BlacklistBase) -> BlacklistResponse:
        blacklist_entry = Blacklist(**blacklist_data.dict())
        db.add(blacklist_entry)
        db.commit()
        db.refresh(blacklist_entry)

        response_data = [
            BlacklistBase(
                userid_fk=blacklist_entry.userid_fk,
                ban_date=blacklist_entry.ban_date,
                ban_reason=blacklist_entry.ban_reason
            )
        ]
        return BlacklistResponse(
            blacklist_list=response_data,
            user_message="User successfully added to blacklist",
            error_status=0,
            system_message="Operation completed"
        )

    @staticmethod
    def delete_blacklist(db: Session, user_id: int) -> dict:
        blacklist_entry = db.query(Blacklist).filter(Blacklist.userid_fk == user_id).first()
        if not blacklist_entry:
            return {"message": "Blacklist entry not found"}
        db.delete(blacklist_entry)
        db.commit()
        return {"message": "Blacklist entry deleted successfully"}
    

    @staticmethod
    def ban_user(db:Session, user_id: int, ban_reason: str):
        blacklist_entry = BlacklistBase(
                userid_fk=user_id,
                ban_date=date.today(),
                ban_reason=ban_reason
        )
        BlacklistCRUD.create_blacklist(db, blacklist_entry)
        AuthCRUD.delete_user(user_id, db)



class ReportCRUD:
    @staticmethod
    def get_reports_by_user(db: Session, current_user_id: int) -> ReportResponse:
        report_entries = (
            db.query(
                Reports.reportid.label("report_id"),
                Reports.reporter,
                Reports.reportee,
                Reports.description,
                Reports.report_date
            )
            .filter(
                (Reports.reporter == current_user_id) |
                (Reports.reportee == current_user_id)
            )
            .all()
        )

        response_data = [
            ReportResponseSchema(
                report_id=entry.report_id,
                reporter=entry.reporter,
                reportee=entry.reportee,
                description=entry.description,
                report_date=entry.report_date
            )
            for entry in report_entries
        ]

        return ReportResponse(
            report_list=response_data,
            user_message="Reports retrieved successfully",
            error_status=0,
            system_message="Operation completed"
        )

    @staticmethod
    def create_report(db: Session, report_data: ReportRequest, current_user_id: int) -> ReportResponseSchema:
        """
        Yeni rapor oluşturma işlemi.
        'reporter' değeri, parametre olarak alınan current_user_id olacak.
        """
        new_report = Reports(
            reporter=current_user_id,
            reportee=report_data.reportee,
            description=report_data.description,
            report_date=date.today()
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        return ReportResponseSchema(
            report_id=new_report.reportid,
            reporter=new_report.reporter,
            reportee=new_report.reportee,
            description=new_report.description,
            report_date=new_report.report_date
        )

    @staticmethod
    def delete_report(db: Session, report_id: int) -> dict:
        """
        Verilen report_id'ye ait kaydı doğrudan siler (herhangi bir yetki kontrolü yapmaz).
        """
        report_entry = db.query(Reports).filter(Reports.reportid == report_id).first()
        if not report_entry:
            return {"message": "Report not found"}
        db.delete(report_entry)
        db.commit()
        return {"message": "Report deleted successfully"}
    
    @staticmethod
    def get_all(db: Session):
        query=(
        db.query(
                Reports.reportid,
                Reports.reporter,
                Reports.reportee,
                Reports.description,
                Reports.report_date
            )
        )
        results = query.all()
        return [
            {
                "report_id" : result.reportid,
                "report_date" : result.report_date,
                "reporter": result.reporter,
                "reportee": result.reportee,
                "description": result.description,
            }
            for result in results
        ]
    

    
        

