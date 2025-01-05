import pytest
from unittest.mock import MagicMock, patch
from fastapi import status
from sqlalchemy.orm import Session
from services.Administration import AdministrationService
from models.User import Users
from schemas.Administration import ReportRequest, ReportResponseSchema  
from crud.Administration import ReportCRUD
from crud.Administration import BlacklistCRUD
from crud.Authentication import AuthCRUD
from tests.conftest import Base, engine, client


class TestAdministrationServices:
    @classmethod
    def setup_class(cls):
        Base.metadata.create_all(bind=engine)

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(bind=engine)

    @patch('crud.Administration.ReportCRUD.create_report')
    def test_report_user_service(self, mock_create_report):
        mock_report = MagicMock(report_id=1)
        mock_create_report.return_value = mock_report

        report_data = ReportRequest(reportee=1, description="Inappropriate behavior")
        response = AdministrationService.report_user_service(report_data, MagicMock(), 2)
        
        assert response.user_message == "User reported successfully, Report ID: 1"
        assert response.error_status == status.HTTP_201_CREATED

    @patch('crud.Administration.ReportCRUD.delete_report')
    def test_delete_report_service_admin(self, mock_delete_report):
        mock_report = MagicMock(reportid=1, reporter=2)

        mock_user_role = True 

        with patch('sqlalchemy.orm.Session.query') as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = mock_report

            response = AdministrationService.delete_report_service(1, MagicMock(), True, 1)

            assert response.user_message == "Report 1 deleted successfully (You are Admin)."
            assert response.error_status == status.HTTP_200_OK

    # @patch('crud.Administration.ReportCRUD.delete_report')
    # def test_delete_report_service_non_admin_authorized(self, mock_delete_report):
    #     mock_report_id = 1 
    #     mock_reporter_id = 1 
    #     mock_user_role = False  
    #     mock_user_id = 1  
    
    #     mock_report = MagicMock(reportid=mock_report_id, reporter=mock_reporter_id)
    
    #     with patch('sqlalchemy.orm.Session.query') as mock_query:
    #         mock_query.return_value.filter.return_value.first.return_value = mock_report
    
    #         with patch.object(ReportCRUD, 'delete_report') as mock_delete_report:
    #             response = AdministrationService.delete_report_service(
    #                 report_id=mock_report_id,
    #                 db=MagicMock(),
    #                 user_role=mock_user_role,
    #                 user_id=mock_user_id
    #             )
    #         assert response.user_message == f"Report {mock_report_id} deleted successfully."
    #         assert response.error_status == status.HTTP_200_OK


    @patch('crud.Administration.ReportCRUD.delete_report')
    def test_delete_report_service_non_admin_not_authorized(self, mock_delete_report):
        mock_report = MagicMock()
        mock_report.reportid = 1
        mock_report.reporter = 2

        mock_user_role = False 
        mock_user_id = 3 

        with patch('sqlalchemy.orm.Session.query') as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = mock_report
            response = AdministrationService.delete_report_service(mock_report.reportid, MagicMock(), mock_user_role, mock_user_id)
            mock_delete_report.assert_not_called()
            assert response.user_message == "You are not authorized to delete this report"
            assert response.error_status == status.HTTP_403_FORBIDDEN

    
    @patch('crud.Administration.ReportCRUD.get_all')
    def test_get_all_reports_admin(self, mock_get_all):
        mock_user_role = True

        mock_reports = [
            ReportResponseSchema(
                report_id=1,
                reporter_id=101,
                reportee_id=102,
                reporter="John Doe",
                reportee="Jane Doe",
                description="Test description",
                report_date="2024-12-27"
            )
        ]

        mock_get_all.return_value = mock_reports

        mock_db = MagicMock()

        response = AdministrationService.get_all_reports(mock_db, mock_user_role)

        assert response.user_message == "Successfully fetched Reports"
        assert response.error_status == 0
        assert response.system_message == "OK"
        assert response.report_list == mock_reports

    def test_get_all_reports_non_admin(mock_db):
        mock_user_role = False

        response = AdministrationService.get_all_reports(mock_db, mock_user_role)
        assert response.user_message == "Only admins can view all reports"
        assert response.error_status == status.HTTP_403_FORBIDDEN

    @patch('crud.Administration.BlacklistCRUD.ban_user')
    @patch('crud.Administration.ReportCRUD.delete_report')
    def test_ban_user_service_admin(self, mock_delete_report, mock_ban_user):
        mock_user_role = True  

        mock_user_id = 1 
        mock_user = MagicMock()
        mock_user.userid = mock_user_id

        existing_reports = [
            MagicMock(reportid=1, reporter=1, reportee=5, description="string", report_date="2024-12-27")
        ]

        with patch('sqlalchemy.orm.Session.query') as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = mock_user
            mock_query.return_value.filter.return_value.all.return_value = existing_reports

            response = AdministrationService.ban_user_service(
                role=mock_user_role,
                user_id=mock_user_id,
                ban_reason="Violation of rules",
                db=MagicMock()
            )
            assert response.user_message == "User successfully banned and all associated reports deleted"
            assert response.error_status == status.HTTP_200_OK


    def test_ban_user_service_non_admin(self):
        mock_user_role = False  

        response = AdministrationService.ban_user_service(mock_user_role, 1, "Spam", MagicMock())
        assert response.user_message == "Only admins can ban users"
        assert response.error_status == status.HTTP_403_FORBIDDEN
