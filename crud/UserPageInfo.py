from sqlalchemy.orm import Session
from models.User import UserPageInfo
from schemas.UserPageInfo import UserPageInfoSchema


from sqlalchemy.orm import Session
from models.User import UserPageInfo, Department
from schemas.UserPageInfo import UserPageInfoResponseSchema

class UserPageInfoCRUD:
    @staticmethod
    def get_user_info_by_id(db: Session, userid: int):
        """
        Fetches UserPageInfo by user ID and joins Department table for department_name.
        """
        query = (
            db.query(
                UserPageInfo.userid_fk,
                UserPageInfo.full_name,
                UserPageInfo.date_of_birth,
                UserPageInfo.gender,
                UserPageInfo.smoking,
                UserPageInfo.pet,
                UserPageInfo.ppurl,
                UserPageInfo.about,
                UserPageInfo.contact,
                UserPageInfo.rh,
                Department.department_name.label("department_name"),
            )
            .join(Department, UserPageInfo.departmentid_fk == Department.departmentid, isouter=True)
            .filter(UserPageInfo.userid_fk == userid)
        ).first()

        if not query:
            return None

        # Convert the query result into a dictionary for the response schema
        user_info_data = {
            "userid_fk": query.userid_fk,
            "full_name": query.full_name,
            "date_of_birth": query.date_of_birth,
            "gender": query.gender,
            "smoking": query.smoking,
            "pet": query.pet,
            "ppurl": query.ppurl,
            "about": query.about,
            "contact": query.contact,
            "rh": query.rh,
            "department_name": query.department_name,
        }

        return UserPageInfoResponseSchema(**user_info_data)
    
    @staticmethod
    def create(db: Session, user_page_info: UserPageInfoSchema):
        """Creates a UserPageInfo record."""
        # Doğrulama
        validated_data = UserPageInfoSchema.model_validate(user_page_info)
        user_info = UserPageInfo(**validated_data.model_dump())
        db.add(user_info)
        db.commit()
        db.refresh(user_info)
        return user_info

    @staticmethod
    def get_by_userid(db: Session, userid: int):
        """Fetches a UserPageInfo record by user ID."""
        return db.query(UserPageInfo).filter(UserPageInfo.userid_fk == userid).first()

    @staticmethod
    def get_ppurl_by_userid(db: Session, userid: int):
        """Fetches the profile picture URL by user ID."""
        return db.query(UserPageInfo.ppurl).filter(UserPageInfo.userid_fk == userid).first

    @staticmethod
    def update(db: Session, userid: int, user_page_info: UserPageInfoSchema):
        """Updates a UserPageInfo record by user ID."""
        db_user_info = db.query(UserPageInfo).filter(UserPageInfo.userid_fk == userid).first()
        if not db_user_info:
            return None
        # Doğrulama
        validated_data = UserPageInfoSchema.model_validate(user_page_info)
        for key, value in validated_data.model_dump(exclude_unset=True).items():
            setattr(db_user_info, key, value)
        db.commit()
        db.refresh(db_user_info)
        return db_user_info

    # @staticmethod
    # def delete(db: Session, userid: int):
    #     """Deletes a UserPageInfo record by user ID."""
    #     db_user_info = db.query(UserPageInfo).filter(UserPageInfo.userid_fk == userid).first()
    #     if not db_user_info:
    #         return None
    #     db.delete(db_user_info)
    #     db.commit()
    #     return db_user_info

    @staticmethod
    def set_rh_status(db: Session, userid: int, rh: bool):
        db_user_info = db.query(UserPageInfo).filter(UserPageInfo.userid_fk == userid).first()
        if not db_user_info:
            return None
        db_user_info.rh = rh
        db.commit()
        db.refresh(db_user_info)
        return db_user_info