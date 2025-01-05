import pytest
from schemas.Administration import BlacklistResponse, ReportResponse, BlacklistBase, ReportResponseSchema
from utils.Administration import create_response_blacklist, create_response_reports
from datetime import date

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
                reporter_id=101,
                reportee_id=102,
                reporter="Reporter Name",
                reportee="Reportee Name",
                description="Test Report Description",
                report_date=date(2024, 12, 27)  # Tarihi string değil, date formatında ver
            )
        ]

        # Fonksiyonu çağır
        response = create_response_reports(user_message, error_status, system_message, report_list)

        # Doğru türde bir nesne döndüğünü kontrol et
        assert isinstance(response, ReportResponse)

        # Kullanıcı mesajını, hata durumunu ve sistem mesajını kontrol et
        assert response.user_message == user_message
        assert response.error_status == error_status
        assert response.system_message == system_message
