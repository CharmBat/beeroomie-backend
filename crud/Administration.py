from sqlalchemy.orm import Session, aliased
from datetime import date
from models.Administration import Blacklist, Reports
from schemas.Administration import BlacklistBase, BlacklistResponse, ReportBase, ReportRequest, ReportResponseSchema, ReportResponse, ReportResponseSchema2
from crud.Authentication import AuthCRUD
from datetime import datetime
from models.User import UserPageInfo

class BlacklistCRUD:
    @staticmethod
    def get_blacklist_by_user(db: Session, e_mail: str) -> BlacklistResponse:
        blacklist_entries = (
            db.query(Blacklist)
            .filter(Blacklist.e_mail == e_mail)
            .all()
        )
        if not blacklist_entries:
            return BlacklistResponse(
                blacklist_list=[],
                user_message="No blacklist entry found for the given email",
                error_status=1,  
                system_message="No matching records found"
            )
        response_data = [
            BlacklistBase(
                e_mail=entry.e_mail,
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
                e_mail=blacklist_entry.e_mail,
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
    def delete_blacklist(db: Session, e_mail: str) -> dict:
        blacklist_entry = db.query(Blacklist).filter(Blacklist.e_mail == e_mail).first()
        if not blacklist_entry:
            return {"message": "Blacklist entry not found"}
        db.delete(blacklist_entry)
        db.commit()
        return {"message": "Blacklist entry deleted successfully"}
    

    @staticmethod
    def ban_user(db:Session, user_id: int, ban_reason: str):
        e_mail = AuthCRUD.get_email_from_userid(user_id, db)
        blacklist_entry = BlacklistBase(
                e_mail=e_mail,
                ban_date=date.today(),
                ban_reason=ban_reason
        )
        response = BlacklistCRUD.create_blacklist(db, blacklist_entry)
        AuthCRUD.delete_user(user_id, db)
        return response



class ReportCRUD:
    @staticmethod
    def get_reports_by_user(db: Session, current_user_id: int) -> ReportResponse:

        reporter_info = aliased(UserPageInfo)
        reportee_info = aliased(UserPageInfo)
    
        report_entries = (
            db.query(
                Reports.reportid.label("report_id"),
                reporter_info.full_name.label("reporter_name"),
                reportee_info.full_name.label("reportee_name"),
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
    def create_report(db: Session, report_data: ReportRequest, current_user_id: int) -> ReportResponseSchema2:
        new_report = Reports(
            reporter=current_user_id,
            reportee=report_data.reportee,
            description=report_data.description,
            report_date=date.today()
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        return ReportResponseSchema2(
            report_id=new_report.reportid,
            reporter=new_report.reporter,
            reportee=new_report.reportee,
            description=new_report.description,
            report_date=new_report.report_date
        )

    @staticmethod
    def delete_report(db: Session, report_id: int) -> dict:
        report_entry = db.query(Reports).filter(Reports.reportid == report_id).first()
        if not report_entry:
            return {"message": "Report not found"}
        db.delete(report_entry)
        db.commit()
        return {"message": "Report deleted successfully"}
    
    @staticmethod
    def get_all(db: Session):
        reporter_info = aliased(UserPageInfo)
        reportee_info = aliased(UserPageInfo)

        query = (
            db.query(
                Reports.reportid,
                reporter_info.full_name.label("reporter_name"),
                reportee_info.full_name.label("reportee_name"),
                Reports.reporter,
                Reports.reportee,
                Reports.description,
                Reports.report_date
            )
            .join(reporter_info, Reports.reporter == reporter_info.userid_fk)
            .join(reportee_info, Reports.reportee == reportee_info.userid_fk)
        )
        results = query.all()

        response_data = [
            ReportResponseSchema(
            report_id=result.reportid,
            reporter=result.reporter_name,
            reportee=result.reportee_name,
            reporter_id=result.reporter,
            reportee_id=result.reportee,
            description=result.description,
            report_date=result.report_date
            )
            for result in results
        ]
        return response_data
    

    
        

