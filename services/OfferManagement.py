from schemas.OfferManagement import OfferResponse, OfferResponseListing
from crud.OfferManagement import OfferCRUD
from fastapi import APIRouter, Depends, HTTPException
from utils.Advertisement import get_user_by_ad
from services.Authentication import get_current_user
class OfferService:
    @staticmethod
    def create_offer_service(adpage_id: int, description: str, db, token: str):
        try:

            offererid_fk = get_current_user(token).userid
            
            offeree_id = get_user_by_ad(db, adpage_id)
            if not offeree_id:
                raise HTTPException(status_code=404, detail="AdPage not found")

            new_offer = OfferCRUD.create(
                db = db,
                offererid_fk=offererid_fk,
                offereeid_fk=offeree_id,
                description=description
            )

            return OfferResponse(
                offer_list=[new_offer],
                user_message=f"Offer {new_offer.offerid} created successfully",
                error_status=0,
                system_message="OK"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            return OfferResponse(
                offer_list=None,
                user_message="Failed to create Offer",
                error_status=500,
                system_message=str(e)
            )
        
    @staticmethod
    def delete_offer_service(offerid: int, db):

        try:
            if not offerid:
                raise HTTPException(status_code=404, detail="Offer not found")
            OfferCRUD.delete(db, offerid)
            
            return OfferResponse(
                user_message=f"Offer {offerid} deleted successfully",
                error_status=0,
                system_message="OK"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            return OfferResponse(
                offer_list=None,
                user_message="Failed to delete Offer",
                error_status=500,
                system_message=str(e)
            )
        
    @staticmethod
    def get_offers_service(token: str, db):
        try:
            offereeid = get_current_user(token).userid
            offers = OfferCRUD.get_all(db, offereeid)
            return OfferResponseListing(
                user_message="Successfully fetched Offers",
                error_status=0,
                system_message="OK",
                offers = offers
            )
        except Exception as e:
            return OfferResponse(
                user_message="Failed to fetch Offers",
                error_status=500,
                system_message=str(e)
            )
        
