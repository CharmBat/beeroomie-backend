from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.UserPageInfo import UserPageInfoSchema, UserPageInfoResponse
from db.database import get_db
from services.UserPageInfo import UserPageInfoService

router = APIRouter(
    prefix="/userpageinfo",
    tags=["UserPageInfo"]
)

@router.post("/", response_model=UserPageInfoResponse)
def create_user_page_info(user_page_info: UserPageInfoSchema, db: Session = Depends(get_db)):
    """
    Creates a new UserPageInfo entry.
    """
    return UserPageInfoService.create_user_page_info_service(user_page_info, db)

@router.get("/{userid}", response_model=UserPageInfoResponse)
def get_user_page_info(userid: int, db: Session = Depends(get_db)):
    """
    Retrieves a UserPageInfo entry by user ID.
    """
    return UserPageInfoService.get_user_page_info_service(userid, db)

@router.put("/{userid}", response_model=UserPageInfoResponse)
def update_user_page_info(userid: int, user_page_info: UserPageInfoSchema, db: Session = Depends(get_db)):
    """
    Updates an existing UserPageInfo entry by user ID.
    """
    return UserPageInfoService.update_user_page_info_service(userid, user_page_info, db)

@router.delete("/{userid}", response_model=UserPageInfoResponse)
def delete_user_page_info(userid: int, db: Session = Depends(get_db)):
    """
    Deletes a UserPageInfo entry by user ID.
    """
    return UserPageInfoService.delete_user_page_info_service(userid, db)
