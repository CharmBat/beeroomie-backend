import pytest
from schemas.Administration import BlacklistResponse, ReportResponse, BlacklistBase, ReportResponseSchema
from utils.Administration import create_response_blacklist, create_response_reports

class TestAdministrationUtils:
    def test_create_response_blacklist(self):
        user_message = "User message"
        error_status = 400
        system_message = "System message"
        blacklist_list = [
            BlacklistBase(
                id=1,
                name="Test User",
                e_mail="testuser@example.com",  
                ban_date="2024-12-27",  
                ban_reason="Violated terms of service" 
            )
        ]

        response = create_response_blacklist(user_message, error_status, system_message, blacklist_list)

        assert isinstance(response, BlacklistResponse)
        assert response.user_message == user_message
        assert response.error_status == error_status
        assert response.system_message == system_message
        assert response.blacklist_list == blacklist_list

    def test_create_response_reports(self):
        user_message = "User message"
        error_status = 400
        system_message = "System message"
        report_list = [
            ReportResponseSchema(
                report_id=1,
                reporter="Reporter Name",
                reportee="Reportee Name",
                description="Test Report Description",
                report_date="2024-12-27"
            )
        ]

        response = create_response_reports(user_message, error_status, system_message, report_list)

        assert isinstance(response, ReportResponse)
        assert response.user_message == user_message
        assert response.error_status == error_status
        assert response.system_message == system_message
        assert response.report_list == report_list