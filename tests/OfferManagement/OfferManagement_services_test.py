import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from crud.OfferManagement import OfferCRUD
from services.OfferManagement import OfferService
from unittest.mock import MagicMock, patch
from fastapi import status
from models.OfferManagement import OfferModel

def test_create_offer_service():
    db = MagicMock()

    adpage_id = 123
    description = "Test offer message"
    userid = 1 

    with patch('crud.Advertisement.AdPageCRUD.get_userid_by_ad', return_value=[2]): 
        mock_adpage = MagicMock()
        mock_adpage.userid_fk = 2 

        db.query().filter().first = MagicMock(return_value=mock_adpage)

        mock_offer = MagicMock()
        mock_offer.offerid = 10 
        OfferCRUD.create = MagicMock(return_value=mock_offer)

        response = OfferService.create_offer_service(adpage_id=adpage_id, description=description, db=db, userid=userid)

        OfferCRUD.create.assert_called_once_with(
            db=db,
            offererid_fk=userid,
            offereeid_fk=2, 
            description=description
        )

        assert response.user_message == "Offer 10 created successfully"
        assert response.error_status == status.HTTP_200_OK
        assert response.system_message == "OK"
    
def test_delete_offer_service():
    db = MagicMock(spec=Session)

    OfferCRUD.delete = MagicMock(return_value=None)

    response = OfferService.delete_offer_service(offerid=1, db=db)

    assert response.user_message == "Offer 1 deleted successfully"
    assert response.error_status == status.HTTP_200_OK
    assert response.system_message == "OK"
    OfferCRUD.delete.assert_called_once_with(db, 1)

def test_get_offers_service():
    db = MagicMock()
    user_id = 2
    OfferCRUD.get_all = MagicMock(return_value=[]) 

    response = OfferService.get_offers_service(db=db, user_id=user_id)

    assert response.user_message == "Successfully fetched Offers"
    assert response.error_status == status.HTTP_200_OK
    assert response.system_message == "OK"
    assert len(response.offers) == 0


def test_create_offer_service_failure_adpage_not_found():
    db = MagicMock()

    adpage_id = 123
    description = "Test offer message"
    userid = 1

    db.query().filter().first.return_value = None

    response = OfferService.create_offer_service(
        adpage_id=adpage_id,
        description=description,
        db=db,
        userid=userid
    )

    assert response.user_message == "AdPage not found"
    assert response.error_status == status.HTTP_404_NOT_FOUND
    assert response.system_message == "AdPage not found"


def test_delete_offer_service_failure_exception():
    db = MagicMock()
    OfferCRUD.delete = MagicMock(side_effect=Exception("Unexpected Error")) 

    response = OfferService.delete_offer_service(offerid=1, db=db)

    assert response.user_message == "Failed to delete Offer"
    assert response.error_status == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Unexpected Error" in response.system_message


def test_get_offers_service_failure_exception():
    db = MagicMock()
    user_id = 2
    OfferCRUD.get_all = MagicMock(side_effect=Exception("Unexpected Error")) 

    response = OfferService.get_offers_service(db=db, user_id=user_id)

    assert response.user_message == "Failed to fetch Offers"
    assert response.error_status == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Unexpected Error" in response.system_message