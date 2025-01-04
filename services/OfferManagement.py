from schemas.OfferManagement import OfferResponse
from crud.OfferManagement import OfferCRUD
from fastapi import APIRouter, Depends, HTTPException
from services.Authentication import AuthenticationService
from crud.Advertisement import AdPageCRUD
from crud.UserPageInfo import UserPageInfoCRUD
from fastapi import status


class OfferService:
    @staticmethod
    def create_offer_service(adpage_id: int, description: str, db, userid: int):
        try:

            offererid_fk = userid
            
            offeree_id = AdPageCRUD.get_userid_by_ad(db, adpage_id)
            if not offeree_id:
                raise HTTPException(status_code=404, detail="AdPage not found")

            new_offer = OfferCRUD.create(
                db = db,
                offererid_fk=offererid_fk,
                offereeid_fk=offeree_id,
                description=description
            )

            return OfferResponse(
                user_message=f"Offer {new_offer.offerid} created successfully",
                error_status=0,
                system_message="OK"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            return OfferResponse(
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
                user_message="Failed to delete Offer",
                error_status=500,
                system_message=str(e)
            )
        
    @staticmethod
    def get_offers_service(db, user_id):
        try:
            rh=UserPageInfoCRUD.get_rh_status_by_userid(db, user_id)
            offers=[]
            if rh:#housie
            #ofreeid=userid olması lazım
                offereeid = user_id
                offers = OfferCRUD.get_all(db, offereeid_fk=offereeid)
            else:#roomie    
            #offererid=userid olması lazım
                offererid = user_id
                offers = OfferCRUD.get_all(db,offererid_fk=offererid)
            
            return OfferResponse(
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
        
