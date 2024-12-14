from sqlalchemy.orm import Session
from models.Advertisement import AdPage,Photos,Neighborhood,District
from models.User import UserPageInfo
from schemas.Advertisement import AdPageSchema,AdListingResponseSchema
from sqlalchemy.orm import Session


class AdPageCRUD:
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
    def get_filtered_ads(db: Session, filters: dict, limit: int = 10, offset: int = 0):
        # Temel sorgu
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
            .join(Neighborhood, AdPage.neighborhoodid_fk == Neighborhood.neighborhoodid)  # Eklenen Join
            .join(District, Neighborhood.districtid_fk == District.districtid)  # Eklenen Join
        )

        # Dinamik filtreleme
        for key, value in filters.items():
            if value is not None:
                if key == "min_price":
                    query = query.filter(AdPage.price >= value)
                elif key == "max_price":
                    query = query.filter(AdPage.price <= value)
                elif key == "neighborhood":
                    query = query.filter(Neighborhood.neighborhood_name.ilike(f"%{value}%"))
                elif key == "district":
                    query = query.filter(District.district_name.ilike(f"%{value}%"))
                elif hasattr(AdPage, key):
                    column = getattr(AdPage, key)
                    query = query.filter(column == value)

        query = query.offset(offset).limit(limit)
        results = query.all()

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
            if result.photourl:
                adpage_dict[adpage_id]["photos"].append(result.photourl)

        return [
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










    @staticmethod
    def get_by_id(db: Session, adpage_id: int):
        return db.query(AdPage).filter(AdPage.adpageid == adpage_id).first()

    @staticmethod
    def create(db: Session, adpage: AdPageSchema) -> AdPage:
        adpage_data = adpage.dict()

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
