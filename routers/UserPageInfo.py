from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.UserPageInfo import UserPageInfoSchema, UserPageInfoResponse
from db.database import get_db
from services.UserPageInfo import UserPageInfoService
from services.Authentication import AuthenticationService
from schemas.Authentication import TokenData
from utils.UserPageInfo import user_page_info_response
from fastapi import status
router = APIRouter(
    prefix="/userpageinfo",
    tags=["UserPageInfo"]
)

@router.post("/", response_model=UserPageInfoResponse)
def create_user_page_info(user_page_info: UserPageInfoSchema, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return UserPageInfoService.create_user_page_info_service(user_page_info, db, current_user.userid)
    else:
        return current_user

@router.get("/{userid}", response_model=UserPageInfoResponse)
def get_user_page_info(userid: int, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return UserPageInfoService.get_user_page_info_service(userid, db)
    else:
        return current_user

@router.put("/", response_model=UserPageInfoResponse)
def update_user_page_info(user_page_info: UserPageInfoSchema, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return UserPageInfoService.update_user_page_info_service(current_user.userid, user_page_info, db)
    else:
        return current_user
@router.delete("/{userid}", response_model=UserPageInfoResponse)
def delete_user_page_info(userid: int, db: Session = Depends(get_db), current_user = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        if current_user.role == True or current_user.userid == userid:
            return UserPageInfoService.delete_user_service(userid=userid,db=db)
        else:
            user_page_info_response(user_message="You are not authorized to delete this user",error_status=status.HTTP_403_FORBIDDEN,system_message="Forbidden")
    else:  
        return current_user
