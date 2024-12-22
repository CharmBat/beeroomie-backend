from fastapi import APIRouter, Depends
from schemas.Advertisement import AdPageSchema, AdPageResponse, AdPageFilterSchema, AdPageRequest, AdPageResponse, AdPageFilterSchema
from services.favorites import favoritesService
from db.database import get_db
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)


@router.get("/{user_id}", response_model=AdPageResponse)
def get_user_favorites(user_id: int, pagination: int = 0, db: Session = Depends(get_db)):
    return favoritesService.get_user_favorites(user_id, db, pagination)

@router.post("/add")
def add_to_favorites(user_id: int, adpage_id: int, db: Session = Depends(get_db)):
    return favoritesService.add_to_favorites(user_id, adpage_id, db)

@router.delete("/remove")
def remove_from_favorites(user_id: int, adpage_id: int, db: Session = Depends(get_db)):
    return favoritesService.remove_from_favorites(user_id, adpage_id, db)