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
    user: TokenData = Depends(AuthenticationService.get_current_user)
):
    return favoritesService.get_user_favorites(user.userid, db, pagination)

@router.post("/")
def add_to_favorites(
    adpage_id: int, 
    db: Session = Depends(get_db), 
    user: TokenData = Depends(AuthenticationService.get_current_user)
):
    return favoritesService.add_to_favorites(user.userid, adpage_id, db)

@router.delete("/")
def remove_from_favorites(
    adpage_id: int, 
    db: Session = Depends(get_db), 
    user: TokenData = Depends(AuthenticationService.get_current_user)
):
    return favoritesService.remove_from_favorites(user.userid, adpage_id, db)

