from sqlalchemy.orm import Session
from models.OfferManagement import OfferModel
from models.User import UserPageInfo
from schemas.OfferManagement import Offer

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
    def get_all(db: Session, offereeid_fk: int=None,offererid_fk:int=None):

        if offereeid_fk:#houise
            query = (
            db.query(
                OfferModel.offerid.label("offer_id"),
                OfferModel.send_message,
                UserPageInfo.full_name.label("other_full_name"),
                UserPageInfo.contact.label("other_contact"),
                OfferModel.offererid_fk.label("other_user_id"),
                UserPageInfo.ppurl.label("other_ppurl")
            )
            .join(UserPageInfo, UserPageInfo.userid_fk == OfferModel.offererid_fk)   
            .filter(OfferModel.offereeid_fk == offereeid_fk)
        )

        elif offererid_fk:#roomie    
            query = (
            db.query(
                OfferModel.offerid.label("offer_id"),
                OfferModel.send_message,
                UserPageInfo.full_name.label("other_full_name"),
                UserPageInfo.contact.label("other_contact"),
                OfferModel.offereeid_fk.label("other_user_id"),
                UserPageInfo.ppurl.label("other_ppurl")
            )
            .join(UserPageInfo, UserPageInfo.userid_fk == OfferModel.offereeid_fk)   
            .filter(OfferModel.offererid_fk == offererid_fk)
        )
        else:
            return None    
        results = query.all()
        offers = []

        for result in results:
            offer = Offer(
            offer_id=result.offer_id,
            send_message=result.send_message,
            offerer_name=result.other_full_name,
            contact_info=result.other_contact,
            other_user_id=result.other_user_id,
            ppurl=result.other_ppurl
            )
            offers.append(offer)
        return offers


        
        
    @staticmethod
    def get_userid_by_offer(db: Session, offerid: int) -> int:
        offer = db.query(OfferModel).filter(OfferModel.offerid == offerid).first()
        if not offer:
            return None
        return offer.offererid_fk




