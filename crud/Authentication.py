from schemas.Authentication import UserInDB


tempDatabase = {
    "gunyel20@itu.edu.tr": {
        "userId": "1",
        "email": "gunyel20@itu.edu.tr",
        "hashed_password": "$2b$12$b1SNnAwbSrjVzFf7D2d9M.izdyr1EY7tSIoWgSyHiiWJdeZbAptpO"
    }
}
db = tempDatabase

def get_user(email: str):
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)
    return None

def add_to_db(email: str, hashed_password: str):
    db[email] = {
        "email": email,
        "hashed_password": hashed_password,
    }