from sqlalchemy.orm import Session
from models.Administration import Blacklist, Reports
from schemas.Administration import BlacklistBase, BlacklistResponse, ReportBase, ReportRequest, ReportResponseSchema, ReportResponse
from crud.Authentication import AuthCRUD
from datetime import datetime

class BlacklistCRUD:
    # Blacklist CRUD Operations
    @staticmethod
    def get_blacklist_by_user(db: Session, user_id: int):
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
            ) for entry in blacklist_entries
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
    def delete_blacklist(db: Session, user_id: int):
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
                ban_date=datetime.datetime.today(),
                ban_reason=ban_reason
        )
        BlacklistCRUD.create_blacklist(db, blacklist_entry)
        AuthCRUD.delete_user(user_id, db)


class ReportsCRUD: 
    # Reports CRUD Operations
    @staticmethod
    def get_reports_by_user(db: Session, user_id: int):
        report_entries = (
            db.query(
                Reports.reportid.label("report_id"),
                Reports.reporter,
                Reports.reportee,
                Reports.description,
                Reports.report_date
            )
            .filter((Reports.reporter == user_id) | (Reports.reportee == user_id))
            .all()
        )
        response_data = [
            ReportResponseSchema(
                report_id=entry.report_id,
                reporter=entry.reporter,
                reportee=entry.reportee,
                description=entry.description,
                report_date=entry.report_date
            ) for entry in report_entries
        ]
        return ReportResponse(
            report_list=response_data,
            user_message="Reports retrieved successfully",
            error_status=0,
            system_message="Operation completed"
        )

    @staticmethod
    def create_report(db: Session, report_data: ReportRequest):
        report_entry = Reports(**report_data.dict())
        db.add(report_entry)
        db.commit()
        db.refresh(report_entry)
        return ReportResponseSchema(
            report_id=report_entry.reportid,
            reporter=report_entry.reporter,
            reportee=report_entry.reportee,
            description=report_entry.description,
            report_date=report_entry.report_date
        )

    @staticmethod
    def delete_report(db: Session, report_id: int):
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
                Reports.reporter,
                Reports.reportee,
                Reports.description
            )
        )
        results = query.all()
        return [
            {
                "reporter": result.reporter,
                "reportee": result.reportee,
                "description": result.description,
            }
            for result in results
        ]
    

    
        

