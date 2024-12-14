from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

# Şifreleme ve doğrulama için PassLib kullanımı
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy kullanıcı veritabanı
user_db = {
    "user1": {
        "password": pwd_context.hash("old_password")  # Eski şifre: "old_password"
    }
}

# İstek modeli
class ChangePasswordRequest(BaseModel):
    username: str
    old_password: str
    new_password: str

@app.post("/change_password")
async def change_password(request: ChangePasswordRequest):
    username = request.username
    old_password = request.old_password
    new_password = request.new_password

    # Kullanıcı kontrolü
    if username not in user_db:
        raise HTTPException(status_code=404, detail="User not found")

    # Eski şifre doğrulama
    if not pwd_context.verify(old_password, user_db[username]["password"]):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # Yeni şifreyi kaydetme
    user_db[username]["password"] = pwd_context.hash(new_password)
    return {"message": "Password changed successfully"}
