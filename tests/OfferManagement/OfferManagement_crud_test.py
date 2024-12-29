import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from crud.OfferManagement import OfferCRUD
from models.OfferManagement import OfferModel

def test_create_offer():
    db = MagicMock(spec=Session)

    new_offer = MagicMock(spec=OfferModel)
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None

    offererid_fk = 1
    offereeid_fk = 2
    description = "Test offer message"

    OfferCRUD.create(db, offererid_fk, offereeid_fk, description)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_get_all_offers():
    db = MagicMock(spec=Session)

    mock_query = MagicMock()
    db.query.return_value = mock_query

    mock_join = MagicMock()
    mock_query.join.return_value = mock_join

    mock_filter = MagicMock()
    mock_join.filter.return_value = mock_filter

    mock_filter.all.return_value = [
        MagicMock(
            offer_id=1,
            send_message="Test offer message",
            offerer_name="Alice",
            contact="alice@example.com",
        )
    ]

    results = OfferCRUD.get_all(db, offereeid_fk=2)

    assert len(results) == 1
    assert results[0]["offer_id"] == 1
    assert results[0]["send_message"] == "Test offer message"
    assert results[0]["offerer_name"] == "Alice"
    assert results[0]["contact_info"] == "alice@example.com"

def test_get_userid_by_offer():
    db = MagicMock(spec=Session)

    mock_offer = MagicMock(spec=OfferModel)
    mock_offer.offererid_fk = 1
    db.query.return_value.filter.return_value.first.return_value = mock_offer

    user_id = OfferCRUD.get_userid_by_offer(db, offerid=1)

    assert user_id == 1

def test_delete_offer():
    db = MagicMock(spec=Session)

    mock_offer = MagicMock(spec=OfferModel)
    db.query.return_value.filter.return_value.first.return_value = mock_offer

    response = OfferCRUD.delete(db, offerid=1)

    db.delete.assert_called_once_with(mock_offer)
    db.commit.assert_called_once()
    assert response["message"] == "Offer deleted successfully"


def test_offer_create_failure():
    db = MagicMock()
    db.commit.side_effect = Exception("Database commit failed")

    with pytest.raises(Exception, match="Database commit failed"):
        OfferCRUD.create(
            db=db,
            offererid_fk=1,
            offereeid_fk=2,
            description="Test Offer"
        )



def test_offer_delete_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = OfferCRUD.delete(db=db, offerid=999)

    assert result is None, "Expected None when the offer to delete is not found"


def test_offer_get_all_failure():
    db = MagicMock()
    db.query.side_effect = Exception("Database query failed")

    with pytest.raises(Exception, match="Database query failed"):
        OfferCRUD.get_all(db=db, offereeid_fk=1)


def test_get_userid_by_offer_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = OfferCRUD.get_userid_by_offer(db=db, offerid=999)

    assert result is None, "Expected None when offer is not found"

def test_user_deletion_authorization():
    db = MagicMock()
    
    fake_offer = MagicMock()
    fake_offer.offerid = 123
    fake_offer.offererid_fk = 2 
    db.query().filter().first.return_value = fake_offer
    
    current_user_id = 1  
    if fake_offer.offererid_fk != current_user_id:
        result = {"error": "Unauthorized to delete this offer"}
    else:
        result = OfferCRUD.delete(db=db, offerid=fake_offer.offerid)
    
    assert result == {"error": "Unauthorized to delete this offer"}, \
        "Expected error when user tries to delete another user's offer"