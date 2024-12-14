from sqlalchemy.orm import Session
from models.Advertisement import AdPage,Photos,AdUtilities, Neighborhood, NumberOfRoom, District, Utilities
from models.User import UserPageInfo
from schemas.Advertisement import AdPageSchema,AdListingResponseSchema, AdPageResponseSchema
from sqlalchemy.orm import Session


class AdPageCRUD:
    @staticmethod
    def get_ad_by_id(db: Session, adpage_id: int):
        if not isinstance(db, Session):
            raise TypeError("db must be an instance of Session")

        query = (
            db.query(
                AdPage.adpageid,
                AdPage.title,
                AdPage.price,
                AdPage.adtype,
                AdPage.m2,
                AdPage.n_floor,
                AdPage.floornumber,
                AdPage.pet,
                AdPage.smoking,
                AdPage.furnished,
                AdPage.description,
                AdPage.address,
                AdPage.gender_choices,
                AdPage.ad_date,
                Neighborhood.neighborhood_name.label("neighborhood"),
                District.district_name.label("district"),
                NumberOfRoom.n_room.label("n_room"),
                UserPageInfo.full_name.label("user_full_name"),
            )
            .join(UserPageInfo, AdPage.userid_fk == UserPageInfo.userid_fk)
            .join(Neighborhood, AdPage.neighborhoodid_fk == Neighborhood.neighborhoodid)
            .join(District, Neighborhood.districtid_fk == District.districtid)
            .join(NumberOfRoom, AdPage.n_roomid_fk == NumberOfRoom.n_roomid)
            .filter(AdPage.adpageid == adpage_id)
        ).first() 

        if not query:
            return None 

        
        photos = (
            db.query(Photos.photourl)
            .filter(Photos.adpageid_fk == adpage_id)
            .all()
        )
        utilities = (
            db.query(Utilities.utility_name)
            .join(AdUtilities, Utilities.utilityid == AdUtilities.utilityid_fk)
            .filter(AdUtilities.adpageid_fk == adpage_id)
            .all()
        )

       
        photo_list = [photo.photourl for photo in photos]
        utility_list = [utility.utility_name for utility in utilities]

        
        ad_data = {
            "adpageid": query.adpageid,
            "title": query.title,
            "price": query.price,
            "adtype": query.adtype,
            "m2": query.m2,
            "n_floor": query.n_floor,
            "floornumber": query.floornumber,
            "pet": query.pet,
            "smoking": query.smoking,
            "furnished": query.furnished,
            "description": query.description,
            "address": query.address,
            "gender_choices": query.gender_choices,
            "ad_date": query.ad_date,
            "neighborhood": query.neighborhood,
            "district": query.district,
            "n_room": query.n_room,
            "user_full_name": query.user_full_name,
            "photos": photo_list,
            "utilities": utility_list,
        }

        return AdPageResponseSchema(**ad_data)

    @staticmethod
    def get_all(db: Session, pagination: int = 0):
        if not isinstance(db, Session):
            raise TypeError("db must be an instance of Session")

       
        query = (
            db.query(
                AdPage.adpageid,
                AdPage.title,
                AdPage.price,
                AdPage.adtype,
                AdPage.address,
                AdPage.pet,
                AdPage.smoking,
                UserPageInfo.full_name,
                Photos.photourl,
            )
            .join(UserPageInfo, AdPage.userid_fk == UserPageInfo.userid_fk)
            .join(Photos, AdPage.adpageid == Photos.adpageid_fk)
            .offset(pagination)
            .limit(10)
        )
        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))
        
        # Fetch all results
        results = query.all()

            
        # Process results into a dictionary structure to group photos 
        adpage_dict = {}
        for result in results:


            adpage_id = result.adpageid

            if adpage_id not in adpage_dict:
                adpage_dict[adpage_id] = {
                    "adpageid": result.adpageid,
                    "adtype": result.adtype,
                    "pet": result.pet,
                    "smoking": result.smoking,
                    "address": result.address,
                    "full_name": result.full_name,
                    "price": result.price,
                    "title": result.title,
                    "photos": [],
                }

            # Add photo URLs
            if result.photourl:
                adpage_dict[adpage_id]["photos"].append(result.photourl)
                
        # Convert to response schema
        adpage_response_schemas = [
            AdListingResponseSchema(
                adpageid=data["adpageid"],
                title=data["title"],
                price=data["price"],
                adtype=data["adtype"],
                pet=data["pet"],
                smoking=data["smoking"],
                address=data["address"],
                full_name=data["full_name"],
                photos=data["photos"],
            )
            for data in adpage_dict.values()
        ]

        return adpage_response_schemas


    @staticmethod
    def get_by_id(db: Session, adpage_id: int):
        return db.query(AdPage).filter(AdPage.adpageid == adpage_id).first()

    @staticmethod
    def create(db: Session, adpage: AdPageSchema) -> AdPage:
        adpage_data = adpage.model_dump()

        adpage_data.pop("adpageid", None)

        db_adpage = AdPage(**adpage_data)

        db.add(db_adpage)
        db.commit()
        db.refresh(db_adpage)

        return db_adpage
    
    @staticmethod
    def update(db: Session, adpage_id: int, adpage: AdPageSchema) -> AdPage:
        db_adpage = db.query(AdPage).filter(AdPage.adpageid == adpage_id).first()
        if not db_adpage:
            return db_adpage
        for key, value in adpage.dict().items():
            setattr(db_adpage, key, value)
        db.commit()
        db.refresh(db_adpage)
        return db_adpage

    @staticmethod
    def delete(db: Session, adpage_id: int):
        db_adpage = db.query(AdPage).filter(AdPage.adpageid == adpage_id).first()
        if not db_adpage:
            return db_adpage
        db.delete(db_adpage)
        db.commit()
        return {"message": "Advertisement deleted successfully"}

class PhotosCRUD:
    @staticmethod
    def create_photos(db: Session, adpage_id: int, photo_urls: list[str]):
        photos = [Photos(adpageid_fk=adpage_id, photourl=url) for url in photo_urls]
        db.bulk_save_objects(photos)  # SQLAlchemy'nin nesne kaydetmesini sağlar
        db.commit()
        return photos

    @staticmethod
    def delete_photos(db: Session, adpage_id: int):
        db.query(Photos).filter(Photos.adpageid_fk == adpage_id).delete()
        db.commit()

class AdUtilitiesCRUD:
    @staticmethod
    def create_ad_utilities(db: Session, adpage_id: int, utility_ids: list[int]):
        # Modeldeki sütun adlarına dikkat edin
        utilities = [
            AdUtilities(adpageid_fk=adpage_id, utilityid_fk=utility_id)
            for utility_id in utility_ids
        ]
        db.bulk_save_objects(utilities)  # SQLAlchemy'nin nesne kaydetmesini sağlar
        db.commit()
        return utilities
   
    @staticmethod
    def delete_ad_utilities(db: Session, adpage_id: int):
        db.query(AdUtilities).filter(AdUtilities.adpageid_fk == adpage_id).delete()
        db.commit()