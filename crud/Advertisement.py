from sqlalchemy.orm import Session
from models.Advertisement import AdPage
from schemas.Advertisement import AdPageSchema

class AdPageCRUD:
    @staticmethod
    def get_all(db: Session):
        return db.query(AdPage).all()

    @staticmethod
    def get_by_id(db: Session, adpage_id: int):
        return db.query(AdPage).filter(AdPage.adpageid == adpage_id).first()

    @staticmethod
    def create(db: Session, adpage: AdPageSchema) -> AdPage:
        adpage_data = adpage.dict()

        adpage_data.pop("adpageid", None)

        db_adpage = AdPage(**adpage_data)
        db.add(db_adpage)
        db.commit()
        db.refresh(db_adpage)

        return db_adpage
    
    @staticmethod
    def update(db: Session, adpage_id: int, adpage: AdPageSchema) -> AdPage:
        db_adpage = db.query(AdPage).filter(AdPage.adpageid == adpage_id).first()
        if not db_adpage:
            return db_adpage
        for key, value in adpage.dict().items():
            setattr(db_adpage, key, value)
        db.commit()
        db.refresh(db_adpage)
        return db_adpage

    @staticmethod
    def delete(db: Session, adpage_id: int):
        db_adpage = db.query(AdPage).filter(AdPage.adpageid == adpage_id).first()
        if not db_adpage:
            return db_adpage
        db.delete(db_adpage)
        db.commit()
        return {"message": "Advertisement deleted successfully"}
    
    




    @staticmethod
    def get_filtered(db: Session, filters: dict):
        filters = {key: value for key, value in filters.items() if value is not None}
        query = db.query(AdPage)

        for key, value in filters.items():
            if key in ["max_price", "min_price"]:  
                continue
            if hasattr(AdPage, key):  
                column = getattr(AdPage, key)
                query = query.filter(column == value)
                
        if "max_price" in filters:
            query = query.filter(AdPage.price <= filters["max_price"])
        if "min_price" in filters:
            query = query.filter(AdPage.price >= filters["min_price"])

        return query

