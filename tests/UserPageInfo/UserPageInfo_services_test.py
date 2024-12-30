from unittest.mock import MagicMock, patch
from services.UserPageInfo import UserPageInfoService
from schemas.UserPageInfo import UserPageInfoSchema, UserPageInfoResponseSchema
from fastapi import status
from datetime import date

class TestUserPageInfoService:
    def test_create_user_page_info_service_success(self):
        db = MagicMock()
        user_info = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Test User",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test about",
            contact="test@test.com",
            rh=True
        )
        
        with patch('crud.UserPageInfo.UserPageInfoCRUD.create') as mock_create:
            mock_create.return_value = MagicMock(userid_fk=1)
            response = UserPageInfoService.create_user_page_info_service(user_info, db, 1)
            
            assert response.error_status == status.HTTP_201_CREATED
            assert "created successfully" in response.user_message
            
    def test_create_user_page_info_service_failure(self):
        db = MagicMock()
        user_info = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Test User",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test about",
            contact="test@test.com",
            rh=True
        )
        
        with patch('crud.UserPageInfo.UserPageInfoCRUD.create') as mock_create:
            mock_create.side_effect = Exception("Database error")
            response = UserPageInfoService.create_user_page_info_service(user_info, db, 1)
            
            assert response.error_status == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Failed to create" in response.user_message
            
    def test_get_user_page_info_service_success(self):
        db = MagicMock()
        # UserPageInfoResponseSchema formatında mock veri oluşturalım
        mock_user_info = UserPageInfoResponseSchema(
            userid_fk=1,
            full_name="Test User",
            department_name="Test Department",  # department_name eklendi
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test about",
            contact="test@test.com",
            rh=True
        )
        
        with patch('crud.UserPageInfo.UserPageInfoCRUD.get_user_info_by_id') as mock_get:
            mock_get.return_value = mock_user_info
            response = UserPageInfoService.get_user_page_info_service(1, db)
            
            assert response.error_status == status.HTTP_200_OK
            assert "retrieved successfully" in response.user_message
            
    def test_get_user_page_info_service_not_found(self):
        db = MagicMock()
        
        with patch('crud.UserPageInfo.UserPageInfoCRUD.get_user_info_by_id') as mock_get:
            mock_get.return_value = None
            response = UserPageInfoService.get_user_page_info_service(999, db)
            
            assert response.error_status == status.HTTP_404_NOT_FOUND
            assert "not found" in response.user_message
            
    def test_update_user_page_info_service_success(self):
        db = MagicMock()
        update_data = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Updated Name",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="new.jpg",
            about="Updated about",
            contact="test@test.com",
            rh=True
        )
        
        with patch('crud.UserPageInfo.UserPageInfoCRUD.get_by_userid') as mock_get:
            with patch('crud.UserPageInfo.UserPageInfoCRUD.update') as mock_update:
                mock_get.return_value = MagicMock(ppurl="old.jpg")
                mock_update.return_value = MagicMock()
                
                response = UserPageInfoService.update_user_page_info_service(1, update_data, db)
                
                assert response.error_status == status.HTTP_200_OK
                assert "updated successfully" in response.user_message
                
    def test_update_user_page_info_service_not_found(self):
        db = MagicMock()
        update_data = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Updated Name",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="new.jpg",
            about="Updated about",
            contact="test@test.com",
            rh=True
        )
        
        with patch('crud.UserPageInfo.UserPageInfoCRUD.get_by_userid') as mock_get:
            mock_get.return_value = None
            
            response = UserPageInfoService.update_user_page_info_service(999, update_data, db)
            
            assert response.error_status == status.HTTP_404_NOT_FOUND
            assert "not found" in response.user_message