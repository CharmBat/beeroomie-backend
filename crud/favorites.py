from sqlalchemy.orm import Session

from models.Advertisement import AdPage,Photos,AdUtilities, Neighborhood, NumberOfRoom, District, Utilities
from models.User import UserPageInfo
from models.favorites import Favorites

class favoritesCRUD:
    @staticmethod
    def get_user_favorites(db: Session, user_id: int, limit: int = 10, offset: int = 0):
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

            .join(Favorites, Favorites.adpageid_fk == AdPage.adpageid) 
            .join(UserPageInfo, AdPage.userid_fk == UserPageInfo.userid_fk)
            .join(Photos, AdPage.adpageid == Photos.adpageid_fk)
            .join(Neighborhood, AdPage.neighborhoodid_fk == Neighborhood.neighborhoodid)
            .join(District, Neighborhood.districtid_fk == District.districtid)
            .filter(Favorites.userid_fk == user_id)
            .offset(offset) 
            .limit(limit)   
        )

        results = query.all()

        # Count the total number of favorite ads for pagination info
        total_count = (
            db.query(Favorites)
            .filter(Favorites.userid_fk == user_id)
            .count()
        )
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

        return list(adpage_dict.values()), total_count
    

    @staticmethod
    def add_to_favorites(db: Session, user_id: int, adpage_id: int):
        try:
            favorite = Favorites(userid_fk=user_id, adpageid_fk=adpage_id)
            db.add(favorite)
            db.commit()
            return {"message": "Advertisement added to favorites successfully.", "status": 200}
        except Exception as e:
            db.rollback()
            return {"message": f"Failed to add to favorites: {str(e)}", "status": 500}
        
        
    @staticmethod
    def remove_from_favorites(db: Session, user_id: int, adpage_id: int):
        try:
            db.query(Favorites).filter(Favorites.userid_fk == user_id, Favorites.adpageid_fk == adpage_id).delete()
            db.commit()
            return {"message": "Advertisement removed from favorites successfully.", "status": 200}
        except Exception as e:
            db.rollback()
            return {"message": f"Failed to remove from favorites: {str(e)}", "status": 500}
