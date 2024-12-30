from utils.UserPageInfo import user_page_info_response
from schemas.UserPageInfo import UserPageInfoResponseSchema
from fastapi import status
from datetime import date

class TestUserPageInfoUtils:
    def test_user_page_info_response_with_data(self):
        test_info = UserPageInfoResponseSchema(
            userid_fk=1,
            full_name="Test Kullanıcı",
            department_name="Test Bölüm",
            date_of_birth=date(1990, 1, 1),
            gender=True,
            smoking=False,
            pet=False,
            ppurl="test.jpg",
            about="Test hakkında",
            contact="test@test.com",
            rh=True
        )
        
        response = user_page_info_response(
            user_message="Başarılı",
            error_status=status.HTTP_200_OK,
            system_message="Test mesaj",
            user_info_list=[test_info]
        )
        
        assert response.user_message == "Başarılı"
        assert response.error_status == status.HTTP_200_OK
        assert response.system_message == "Test mesaj"
        assert len(response.user_info_list) == 1
        assert response.user_info_list[0].userid_fk == 1

    def test_user_page_info_response_without_data(self):
        response = user_page_info_response(
            user_message="Veri bulunamadı",
            error_status=status.HTTP_404_NOT_FOUND,
            system_message="Test hata",
            user_info_list=None
        )
        
        assert response.user_message == "Veri bulunamadı"
        assert response.error_status == status.HTTP_404_NOT_FOUND
        assert response.system_message == "Test hata"
        assert response.user_info_list is None