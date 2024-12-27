from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from crud.OfferManagement import OfferCRUD
from services.OfferManagement import OfferService
from schemas.OfferManagement import OfferResponse, OfferResponseListing
from models.OfferManagement import OfferModel
from utils.Advertisement import get_user_by_ad
from unittest.mock import MagicMock, patch

def test_create_offer_service():
    db = MagicMock()

    adpage_id = 123
    description = "Test offer message"
    userid = 1  
    with patch('utils.Advertisement.get_user_by_ad', return_value=2):  
        mock_adpage = MagicMock()
        mock_adpage.userid_fk = 2  # `userid_fk` alanını burada ayarlıyoruz
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
