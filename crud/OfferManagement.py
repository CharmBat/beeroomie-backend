from sqlalchemy.orm import Session
from models.OfferManagement import OfferModel

class OfferCRUD:
    @staticmethod
    def create(db: Session, offererid_fk: int, offereeid_fk: int, description: str) -> OfferModel:
        new_offer = OfferModel(
            offererid_fk=offererid_fk, 
            offereeid_fk=offereeid_fk,  
            send_message=description
        )
        db.add(new_offer)
        db.commit()
        db.refresh(new_offer)
        return new_offer



