
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from crud.Administration import BlacklistCRUD, ReportCRUD, BlacklistBase
from schemas.Administration import ReportRequest
from datetime import date
from models.Administration import Reports

def test_get_blacklist_by_user():
    db = MagicMock(spec=Session)
    
    mock_entry = MagicMock()
    mock_entry.e_mail = "test@example.com"
    mock_entry.ban_date = date.today()
    mock_entry.ban_reason = "Spam"
    
    db.query().filter().all.return_value = [mock_entry]  # `db.query().filter().all()`'ı mock'la

    response = BlacklistCRUD.get_blacklist_by_user(db, "test@example.com")

    assert response.user_message == "Blacklist data retrieved successfully"
    assert response.error_status == 0
    assert len(response.blacklist_list) == 1
    assert response.blacklist_list[0].e_mail == "test@example.com"


def test_create_blacklist():
    db = MagicMock(spec=Session)
    
    blacklist_data = BlacklistBase(e_mail="test@example.com", ban_date=date.today(), ban_reason="Spam")
    
    response = BlacklistCRUD.create_blacklist(db, blacklist_data)

    assert response.user_message == "User successfully added to blacklist"
    assert response.error_status == 0


def test_delete_blacklist():
    db = MagicMock(spec=Session)
    
    mock_entry = MagicMock()
    mock_entry.e_mail = "test@example.com"
    db.query().filter().first.return_value = mock_entry  # Mock veri döndürülmesi
    
    response = BlacklistCRUD.delete_blacklist(db, "test@example.com")

    assert response["message"] == "Blacklist entry deleted successfully"


def test_ban_user():
    db = MagicMock(spec=Session)

    with patch("crud.Authentication.AuthCRUD.get_email_from_userid", return_value="test@example.com"):
        with patch("crud.Authentication.AuthCRUD.delete_user"):
            response = BlacklistCRUD.ban_user(db, 1, "Violation of terms")

    assert response.user_message == "User successfully added to blacklist"

def test_get_reports_by_user():
    db = MagicMock(spec=Session)

    mock_report = MagicMock()
    mock_report.reportid = 1
    mock_report.reporter = "John Doe"
    mock_report.reportee = "Alice Mavis"
    mock_report.description = "Inappropriate behavior"
    mock_report.report_date = date.today()
    
    db.query().filter().all.return_value = [mock_report]  

    response = ReportCRUD.get_reports_by_user(db, 1)

    assert response.user_message == "Reports retrieved successfully"
    assert response.error_status == 0
    assert len(response.report_list) == 1
    assert response.report_list[0].report_id == 1
    assert response.report_list[0].reporter == "John Doe"


def test_create_report():
    db = MagicMock(spec=Session)

    report_data = ReportRequest(reportee=2, description="Spam activity")

    new_report = MagicMock(spec=Reports)
    new_report.reportid = None 
    new_report.report_date = date.today()

    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None

    db.add(new_report)

    new_report.reportid = 1
    db.refresh(new_report)

    response = ReportCRUD.create_report(db, report_data, 1)

    assert response.report_id == None  
    assert response.reporter == 1
    assert response.reportee == 2
    assert response.description == "Spam activity"

def test_delete_report():
    db = MagicMock(spec=Session)

    mock_report = MagicMock()
    mock_report.reportid = 1
    db.query().filter().first.return_value = mock_report  
    
    response = ReportCRUD.delete_report(db, 1)

    assert response["message"] == "Report deleted successfully"

def test_get_all_reports():
    db = MagicMock(spec=Session)

    mock_report = MagicMock()
    mock_report.reportid = 1
    mock_report.report_date = date.today()
    mock_report.reporter_name = "John Doe"
    mock_report.reportee_name = "Jane Doe"
    mock_report.description = "Spam activity"
    db.query().join().join().all.return_value = [mock_report] 
    response = ReportCRUD.get_all(db)

    assert len(response) == 1
    assert response[0]["report_id"] == 1
    assert response[0]["reporter"] == "John Doe"

