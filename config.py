from dotenv import load_dotenv
import os

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
VERIFICATION_KEY = os.getenv("VERIFICATION_KEY")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES"))
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_SSL=os.getenv("DB_SSL")

MAIL_USERNAME=os.getenv("MAIL_USERNAME")
MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")

MAIL_FROM=os.getenv("MAIL_FROM")
MAIL_PORT=os.getenv("MAIL_PORT")
MAIL_SERVER=os.getenv("MAIL_SERVER")


