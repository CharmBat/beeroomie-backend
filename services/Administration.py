from crud.Administration import BlacklistCRUD, ReportsCRUD
from schemas.Administration import ReportRequest, ReportResponse, ReportResponseSchema
from fastapi import status
from utils.Administration import create_response_reports

class AdministrationService:
    @staticmethod
    def report_user_service(report_data: ReportRequest, db):
        try:
            # Kullanıcıyı rapor et
            report = ReportsCRUD.create_report(db, report_data)

            return create_response_reports(
                user_message=f"User reported successfully, Report ID: {report.report_id}",
                error_status=status.HTTP_201_CREATED,
                system_message="OK",
                report_list=[report]
            )
        except Exception as e:
            return create_response_reports(
                user_message="Failed to report user",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e),
                report_list=None
            )

    @staticmethod
    def delete_report_service(report_id: int, db):
        try:
            # Raporu kontrol et
            report = ReportsCRUD.get_reports_by_user(db, report_id)
            if not report:
                return create_response_reports(
                    user_message="Report not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No report found with the given ID",
                    report_list=None
                )

            # Raporu sil
            ReportsCRUD.delete_report(db, report_id)
            return create_response_reports(
                user_message=f"Report {report_id} deleted successfully",
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
    def get_all_reports(db):
        try:
            reports = ReportsCRUD.get_all(db)
            return create_response_reports(
                user_message="Successfully fetched Reports",
                error_status=0,
                system_message="OK",
                report_list = reports
            )
        except Exception as e:
            return create_response_reports(
                user_message="Failed to fetch Reports",
                error_status=500,
                system_message=str(e)
            )
        

    @staticmethod
    def ban_user_service(user_id: int, ban_reason: str, db):
        try:
            user = user_id
            if not user:
                return create_response_reports(
                    user_message="Report not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="No report found with the given ID",
                    report_list=None
                )

            ReportsCRUD.ban_user(db, user_id, ban_reason)
            return create_response_reports(
                user_message="Successfully banned user",
                error_status=0,
                system_message="OK",
                report_list = None
            )
        except Exception as e:
            return create_response_reports(
                user_message="Failed to ban user",
                error_status=500,
                system_message=str(e)
            )
  


