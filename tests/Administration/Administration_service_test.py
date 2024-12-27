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

@pytest.fixture
def mock_db():
    return MagicMock(Session)


@pytest.fixture
def mock_report_data():
    return ReportRequest(
        reportee=1,
        description="Inappropriate behavior"
    )

@pytest.fixture
def mock_user():
    return MagicMock(Users)

def test_report_user_service(mock_db, mock_report_data):
    mock_report = MagicMock()
    mock_report.report_id = 1

    with patch.object(ReportCRUD, 'create_report', return_value=mock_report):
        response = AdministrationService.report_user_service(mock_report_data, mock_db, 2)
        assert response.user_message == "User reported successfully, Report ID: 1"
        assert response.error_status == status.HTTP_201_CREATED


def test_delete_report_service_admin(mock_db):
    mock_report = MagicMock()
    mock_report.reportid = 1
    mock_report.reporter = 2

    mock_user_role = True 

    with patch.object(mock_db, 'query', return_value=MagicMock(first=MagicMock(return_value=mock_report))):
        with patch.object(ReportCRUD, 'delete_report') as mock_delete_report:
            response = AdministrationService.delete_report_service(1, mock_db, mock_user_role, 1)
            mock_delete_report.assert_called_once()  
            assert response.user_message == "Report 1 deleted successfully (You are Admin)."
            assert response.error_status == status.HTTP_200_OK

def test_delete_report_service_non_admin_authorized(mock_db):
    mock_report_id = 1  
    mock_reporter_id = 2
    mock_user_role = False  
    mock_user_id = 2

    mock_report = MagicMock()
    mock_report.reportid = mock_report_id
    mock_report.reporter = mock_reporter_id

    with patch.object(mock_db, 'query') as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = mock_report

        with patch.object(ReportCRUD, 'delete_report') as mock_delete_report:
            response = AdministrationService.delete_report_service(
                report_id=mock_report_id,
                db=mock_db,
                user_role=mock_user_role,
                user_id=mock_user_id
            )

            mock_delete_report.assert_called_once_with(mock_db, mock_report_id)

            assert response.user_message == f"Report {mock_report_id} deleted successfully."
            assert response.error_status == status.HTTP_200_OK

def test_delete_report_service_non_admin_not_authorized(mock_db):
    mock_report = MagicMock()
    mock_report.reportid = 1
    mock_report.reporter = 2

    mock_user_role = False 
    mock_user_id = 3 

    with patch.object(mock_db, 'query', return_value=MagicMock(first=MagicMock(return_value=mock_report))):
        response = AdministrationService.delete_report_service(1, mock_db, mock_user_role, mock_user_id)
        assert response.user_message == "You are not authorized to delete this report"
        assert response.error_status == status.HTTP_403_FORBIDDEN

def test_get_all_reports_admin(mock_db):
    mock_user_role = True 

    mock_reports = [
        ReportResponseSchema(
            report_id=1,
            reporter="reporter1",
            reportee="reportee1",
            description="string",
            report_date="2024-12-27"
        )
    ]

    with patch.object(ReportCRUD, 'get_all', return_value=mock_reports) as mock_get_all:
        response = AdministrationService.get_all_reports(mock_db, mock_user_role)
        mock_get_all.assert_called_once_with(mock_db)

        assert response.user_message == "Successfully fetched Reports"
        assert response.error_status == 0
        assert response.system_message == "OK"
        assert response.report_list == mock_reports


def test_get_all_reports_non_admin(mock_db):
    mock_user_role = False

    response = AdministrationService.get_all_reports(mock_db, mock_user_role)
    assert response.user_message == "Only admins can view all reports"
    assert response.error_status == status.HTTP_403_FORBIDDEN


def test_ban_user_service_admin(mock_db):
    mock_user_role = True  

    mock_user_id = 1 
    mock_user = MagicMock()
    mock_user.userid = mock_user_id

    existing_reports = [
        MagicMock(reportid=1, reporter=1, reportee=5, description="string", report_date="2024-12-27")
    ]

    with patch.object(mock_db, 'query') as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = mock_user
        mock_query.return_value.filter.return_value.all.return_value = existing_reports

        with patch.object(ReportCRUD, 'delete_report') as mock_delete_report:
            with patch.object(BlacklistCRUD, 'ban_user') as mock_ban_user:
                with patch.object(AuthCRUD, 'delete_user') as mock_delete_user:
                    response = AdministrationService.ban_user_service(
                        role=mock_user_role,
                        user_id=mock_user_id,
                        ban_reason="Violation of rules",
                        db=mock_db
                    )
                    assert mock_delete_report.call_count == len(existing_reports)

                    for report in existing_reports:
                        mock_delete_report.assert_any_call(mock_db, report.reportid)

                    mock_ban_user.assert_called_once_with(mock_db, mock_user_id, "Violation of rules")

                    mock_delete_user.assert_called_once_with(mock_user_id, mock_db)

                    assert response.user_message == "User successfully banned and all associated reports deleted"
                    assert response.error_status == status.HTTP_200_OK



def test_ban_user_service_non_admin(mock_db):
    mock_user_role = False  

    response = AdministrationService.ban_user_service(mock_user_role, 1, "Spam", mock_db)
    assert response.user_message == "Only admins can ban users"
    assert response.error_status == status.HTTP_403_FORBIDDEN
