from sqlalchemy.orm import Session
from models.User import Users
from schemas.Authentication import UserInDB
class AuthCRUD:

    @staticmethod
    def get_user(email: str,db:Session): #get user from db who has the given email and confirmed
        try:
            user=db.query(Users).filter(Users.e_mail==email,Users.is_confirmed==True).first()
            curret_user=UserInDB(userid=user.userid,e_mail=user.e_mail,role=user.role,hashed_password=user.hashed_password,is_confirmed=user.is_confirmed)
            if user:
                return curret_user
            return None
                
        except Exception as e:
            print(f"Database error in get_user: {e}")
            return None

            
    @staticmethod
    def add_user_to_db(email: str, hashed_password: str,db:Session):
        try:
            db.add(Users(e_mail=email,hashed_password=hashed_password,is_confirmed=False,role=False))
            db.commit()
        except Exception as e:
            print(f"Database error in add_user_to_db: {e}")

    @staticmethod
    def confirm_user(userid: str,db:Session):

        try:
            user = db.query(Users).filter(Users.userid == userid).first()
            if user:
                db.query(Users).filter(Users.userid == userid).update({"is_confirmed": True})
                db.commit()
                print(f"User with userid {userid} confirmed successfully.")
                return True
            else:
                print(f"No user found with userid {userid}.")
                return False

        except Exception as e:
            print(f"Database error in confirm_user: {e}")
            return False

    @staticmethod
    def delete_user(userid: str,db:Session):
        try:
            user=db.query(Users).filter(Users.userid == userid).first()
            if user:
                db.query(Users).filter(Users.userid == userid).delete()
                db.commit()
                print(f"User with userid {userid} deleted successfully.")
            else:
                print(f"No user found with userid {userid}.")    

        except Exception as e:
            print(f"Database error in delete_user: {e}")
            return None

    @staticmethod
    def update_user_password(userid: str, hashed_password: str,db:Session):

        try:
            user=db.query(Users).filter(Users.userid == userid).first()
            
            if user:
                db.query(Users).filter(Users.userid == userid).update({"hashed_password": hashed_password})
                db.commit()
                print(f"Password updated successfully for user with userid {userid}.")
            else:
               print(f"No user found with userid {userid}.")

        except Exception as e:
            print(f"Database error in update_user_password: {e}")
            return None

    @staticmethod
    def get_userid_from_email(email: str,db:Session):
        try:
            user=db.query(Users).filter(Users.e_mail == email).first()
            if user:
                return user.userid
            return None
        except Exception as e:
            print(f"Database error in get_userid_from_email: {e}")
            return None

    @staticmethod
    def confirm_user(email: str,db:Session):
        try:
            user=db.query(Users).filter(Users.e_mail == email).first()

            if user:
                db.query(Users).filter(Users.e_mail == email).update({"is_confirmed": True})
                db.commit()
                print(f"User with email {email} confirmed successfully.")
            else:
                print(f"No user found with email {email}.")    
              
        except Exception as e:
            print(f"Database error in confirm_user: {e}")
            return None
