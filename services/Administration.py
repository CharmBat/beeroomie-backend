from fastapi import status
from sqlalchemy.orm import Session
from utils.Administration import create_response_reports
from crud.Administration import ReportCRUD
from crud.Administration import BlacklistCRUD
from crud.Authentication import AuthCRUD
from schemas.Administration import ReportRequest
from schemas.Authentication import TokenData
from models.Administration import Reports
from models.User import Users


class AdministrationService:
    @staticmethod
    def report_user_service(report_data: ReportRequest, db: Session, current_user) -> dict:
        try:
            report = ReportCRUD.create_report(
                db=db,
                report_data=report_data,
                current_user_id=current_user.userid  # user ID
            )

            return create_response_reports(
                user_message=f"User reported successfully, Report ID: {report.report_id}",
                error_status=status.HTTP_201_CREATED,
                system_message="OK",
                report_list=None  # veya [report] denilebilir
            )

        except Exception as e:
            return create_response_reports(
                user_message="Failed to report user",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
                report_list=None
            )

    @staticmethod
    def delete_report_service(report_id: int, db: Session, current_user) -> dict:
        """
        Rapor silme işlemi.
        - Admin (current_user.role == True) her raporu silebilir.
        - Admin değilse sadece kendi raporu silebilir.
        """
        try:
            # 1) Silinecek rapor var mı?
            report_entry = db.query(Reports).filter(Reports.reportid == report_id).first()
            if not report_entry:
                return create_response_reports(
                    user_message="Report not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No report found with the given ID",
                    report_list=None
                )

            # 2) Admin ise doğrudan silebilsin
            if current_user.role is True:
                ReportCRUD.delete_report(db, report_id)
                return create_response_reports(
                    user_message=f"Report {report_id} deleted successfully (You are Admin).",
                    error_status=status.HTTP_200_OK,
                    system_message="OK",
                    report_list=None
                )
            else:
                # Admin değil -> sadece raporu yazan kişi silebilsin
                if report_entry.reporter != current_user.userid:
                    return create_response_reports(
                        user_message="You are not authorized to delete this report",
                        error_status=status.HTTP_403_FORBIDDEN,
                        system_message="Only the report owner or an admin can delete a report",
                        report_list=None
                    )
                ReportCRUD.delete_report(db, report_id)
                return create_response_reports(
                    user_message=f"Report {report_id} deleted successfully.",
                    error_status=status.HTTP_200_OK,
                    system_message="OK",
                    report_list=None
                )

        except Exception as e:
            return create_response_reports(
                user_message="Failed to delete report",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
                report_list=None
            )
        
    @staticmethod
    def get_all_reports(db: Session):
        try:
            reports = ReportCRUD.get_all(db)
            return create_response_reports(
                user_message="Successfully fetched Reports",
                error_status=0,
                system_message="OK",
                report_list=reports
            )
        except Exception as e:
            return create_response_reports(
                user_message="Failed to fetch Reports",
                error_status=500,
                system_message=str(e),
            )
        

    @staticmethod
    def ban_user_service(token: TokenData, user_id: int, ban_reason: str, db: Session):
        try:
            if not token.role:
                return {
                    "user_message": "Only admins can ban users",
                    "error_status": status.HTTP_403_FORBIDDEN,
                    "system_message": "User is not an admin",
                }

            user = db.query(Users).filter(Users.userid == user_id).first()
            if not user:
                return {
                    "user_message": "User not found",
                    "error_status": status.HTTP_404_NOT_FOUND,
                    "system_message": "User does not exist",
                }

            reports = db.query(Reports).filter(
                (Reports.reporter == user_id) | (Reports.reportee == user_id)
            ).all()
            for report in reports:
                ReportCRUD.delete_report(db, report.reportid)

            BlacklistCRUD.ban_user(db, user_id, ban_reason)
            AuthCRUD.delete_user(user_id, db)

            return {
                "user_message": "User successfully banned and all associated reports deleted",
                "error_status": status.HTTP_200_OK,
                "system_message": "Operation successful",
            }

        except Exception as e:
            return {
                "user_message": "Failed to ban user",
                "error_status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "system_message": str(e),
            }

  


