from sqlalchemy.orm import Session
from models.OfferManagement import OfferModel
from models.User import UserPageInfo

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
    
    @staticmethod
    def delete(db: Session, offerid: int):
        offer = db.query(OfferModel).filter(OfferModel.offerid == offerid).first()
        if not offer:
            return offer
        db.delete(offer)
        db.commit()
        return {"message": "Offer deleted successfully"}
    
    @staticmethod
    def get_all(db: Session, offereeid_fk: int):
        query = (
            db.query(
                OfferModel.offerid.label("offer_id"),
                OfferModel.send_message,
                UserPageInfo.full_name.label("offerer_name"),
                UserPageInfo.contact
            )
            .join(UserPageInfo, UserPageInfo.userid_fk == OfferModel.offererid_fk)   
        )
        
        results = query.all()
        return [
            {
                "offer_id": result.offer_id,
                "send_message": result.send_message,
                "offerer_name": result.offerer_name,
                "contact_info": result.contact,
            }
            for result in results
        ]
            




