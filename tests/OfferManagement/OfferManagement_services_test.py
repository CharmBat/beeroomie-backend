import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from crud.OfferManagement import OfferCRUD
from services.OfferManagement import OfferService
from models.OfferManagement import OfferModel
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

def test_create_offer_service():
    db = MagicMock()

    adpage_id = 123
    description = "Test offer message"
    userid = 1  
    with patch('crud.Advertisement.AdPageCRUD.get_userid_by_ad', return_value=2):  
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
        assert response.error_status == 0
        assert response.system_message == "OK"
    
def test_delete_offer_service():
    db = MagicMock(spec=Session)

    OfferCRUD.delete = MagicMock(return_value={"message": "Offer deleted successfully"})

    response = OfferService.delete_offer_service(offerid=1, db=db)

    assert response.user_message == "Offer 1 deleted successfully"
    assert response.error_status == 0
    assert response.system_message == "OK"
    OfferCRUD.delete.assert_called_once_with(db, 1)

def test_get_offers_service():
    db = MagicMock(spec=Session)
    user_id = 2  
    mock_offer = OfferModel()
    mock_offer.offerid = 1
    mock_offer.offererid_fk = 3
    mock_offer.offereeid_fk = user_id
    mock_offer.send_message = "Test offer message"

    OfferCRUD.get_all = MagicMock(return_value=[
    {
        "offer_id": 1,
        "send_message": "Test offer message",
        "offerer_name": "Alice",
        "contact_info": "alice@example.com",
    }
])

    try:
        response = OfferService.get_offers_service(token="dummy_token", db=db, user_id=user_id)
    except Exception as e:
        print(f"Error occurred: {e}")
    assert response.user_message == "Successfully fetched Offers"
    assert response.error_status == 0
    assert response.system_message == "OK"

    assert len(response.offers) == 1

    offer = response.offers[0]
    assert offer.offer_id == 1
    assert offer.send_message == "Test offer message"

    OfferCRUD.get_all.assert_called_once_with(db, user_id)



def test_create_offer_service_failure_adpage_not_found():
    db = MagicMock()

    adpage_id = 123
    description = "Test offer message"
    userid = 1

    db.query().filter().first.return_value = None

    with patch('crud.Advertisement.AdPageCRUD.get_userid_by_ad', wraps=lambda db, adpage_id: None):
        try:
            OfferService.create_offer_service(
                adpage_id=adpage_id,
                description=description,
                db=db,
                userid=userid
            )
        except HTTPException as e:
            assert e.status_code == 404
            assert e.detail == "AdPage not found"
        else:
            assert False, "HTTPException was not raised as expected"



def test_delete_offer_service_failure_exception():
    db = MagicMock()
    OfferCRUD.delete = MagicMock(side_effect=Exception("Unexpected Error")) 

    response = OfferService.delete_offer_service(offerid=1, db=db)

    assert response.user_message == "Failed to delete Offer"
    assert response.error_status == 500
    assert "Unexpected Error" in response.system_message

def test_get_offers_service_failure_empty_offers():
    db = MagicMock()
    user_id = 2
    OfferCRUD.get_all = MagicMock(return_value=[]) 

    response = OfferService.get_offers_service(token="dummy_token", db=db, user_id=user_id)

    assert response.user_message == "Successfully fetched Offers"
    assert response.error_status == 0
    assert response.system_message == "OK"
    assert len(response.offers) == 0

def test_get_offers_service_failure_exception():
    db = MagicMock()
    user_id = 2
    OfferCRUD.get_all = MagicMock(side_effect=Exception("Unexpected Error")) 

    response = OfferService.get_offers_service(token="dummy_token", db=db, user_id=user_id)

    assert response.user_message == "Failed to fetch Offers"
    assert response.error_status == 500
    assert "Unexpected Error" in response.system_message