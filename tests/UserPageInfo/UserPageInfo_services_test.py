from unittest.mock import patch, MagicMock
from ..conftest import Base, engine, client
from services.UserPageInfo import UserPageInfoService
from schemas.UserPageInfo import UserPageInfoSchema, UserPageInfoResponseSchema
from fastapi import status
from datetime import date

class TestUserPageInfoServices:
    @classmethod
    def setup_class(cls):
        Base.metadata.create_all(bind=engine)

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(bind=engine)

    @patch('services.UserPageInfo.UserPageInfoCRUD.create')
    def test_create_user_page_info_success(self, mock_create):
        # Authentication testlerindeki gibi basit mock yapılandırması
        mock_file = MagicMock()
        mock_file.content_type = "image/jpeg"  # content_type özelliğini ekleyin
        mock_file.filename = "test.jpg"        # filename özelliğini ekleyin


        mock_create.return_value = MagicMock(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Test Kullanıcı",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )

        user_info = UserPageInfoSchema(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Test Kullanıcı",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        
        
        response = UserPageInfoService.create_user_page_info_service(
            user_info, MagicMock(), 1
        )
        
        assert response.error_status == status.HTTP_201_CREATED

    @patch('services.UserPageInfo.UserPageInfoCRUD.get_by_userid')
    def test_get_user_page_info_success(self, mock_get):
        mock_get.return_value = MagicMock(
            userid_fk=1,
            departmentid_fk=1,
            full_name="Test Kullanıcı",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        
        response = UserPageInfoService.get_user_page_info_service(1, MagicMock())
        assert response.error_status == status.HTTP_200_OK

    @patch('services.UserPageInfo.UserPageInfoCRUD.get_by_userid')
    def test_get_user_page_info_not_found(self, mock_get):
        mock_get.return_value = None
        
        response = UserPageInfoService.get_user_page_info_service(999, MagicMock())
        assert response.error_status == status.HTTP_404_NOT_FOUND