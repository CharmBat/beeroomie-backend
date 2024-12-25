from fastapi import APIRouter, Depends
from schemas.Advertisement import  AdPageResponse, AdPageResponse
from schemas.Authentication import TokenData
from services.Authentication import AuthenticationService
from services.favorites import favoritesService
from db.database import get_db
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)


@router.get("/", response_model=AdPageResponse)
def get_user_favorites(pagination: int = 0, db: Session = Depends(get_db), 
    current_user: TokenData = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return favoritesService.get_user_favorites(current_user.userid, db, pagination)
    else:
        return current_user

@router.post("/")
def add_to_favorites(
    adpage_id: int, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return favoritesService.add_to_favorites(current_user.userid, adpage_id, db)
    else:
        return current_user
    

@router.delete("/")
def remove_from_favorites(
    adpage_id: int, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(AuthenticationService.get_current_user)):
    if isinstance(current_user, TokenData):
        return favoritesService.remove_from_favorites(current_user.userid, adpage_id, db)
    else:
        return current_user
    

