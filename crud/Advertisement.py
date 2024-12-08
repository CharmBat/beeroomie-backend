from sqlalchemy.orm import Session
from models.Advertisement import AdPage
from schemas.Advertisement import AdPageSchema

class AdPageCRUD:
    @staticmethod
    def get_all(db: Session):
        return db.query(AdPage).all()

    @staticmethod
    def get_by_id(db: Session, adpage_id: int):
        return db.query(AdPage).filter(AdPage.adpageID == adpage_id).first()

    @staticmethod
    def create(db: Session, adpage: AdPageSchema) -> AdPage:
        db_adpage = AdPage(**adpage.dict())
        db.add(db_adpage)
        db.commit()
        db.refresh(db_adpage)
        return db_adpage

    @staticmethod
    def update(db: Session, adpage_id: int, adpage: AdPageSchema) -> AdPage:
        db_adpage = db.query(AdPage).filter(AdPage.adpageID == adpage_id).first()
        if not db_adpage:
            return db_adpage
        for key, value in adpage.dict().items():
            setattr(db_adpage, key, value)
        db.commit()
        db.refresh(db_adpage)
        return db_adpage

    @staticmethod
    def delete(db: Session, adpage_id: int):
        db_adpage = db.query(AdPage).filter(AdPage.adpageID == adpage_id).first()
        if not db_adpage:
            raise HTTPException(status_code=404, detail="AdPage not found")
        db.delete(db_adpage)
        db.commit()
        return {"message": "AdPage deleted successfully"}
