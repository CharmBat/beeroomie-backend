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
            
            offeree_row = AdPageCRUD.get_userid_by_ad(db, adpage_id)
            if not offeree_row:
                return OfferResponse(
                    user_message="AdPage not found",
                    error_status=status.HTTP_404_NOT_FOUND,
                    system_message="AdPage not found"
                )

            offeree_id = offeree_row[0]
            new_offer = OfferCRUD.create(
                db = db,
                offererid_fk=offererid_fk,
                offereeid_fk=offeree_id,
                description=description
            )

            return OfferResponse(
                user_message=f"Offer {new_offer.offerid} created successfully",
                error_status=status.HTTP_200_OK,
                system_message="OK"
            )
        except Exception as e:
            return OfferResponse(
                user_message="Failed to create Offer",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
                error_status=status.HTTP_200_OK,
                system_message="OK"
            )
        except Exception as e:
            return OfferResponse(
                user_message="Failed to delete Offer",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
                error_status=status.HTTP_200_OK,
                system_message="OK",
                offers = offers
            )
        except Exception as e:
            return OfferResponse(
                user_message="Failed to fetch Offers",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e)
            )
        
