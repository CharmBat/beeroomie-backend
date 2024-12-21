from fastapi import FastAPI
from routers import Authentication, Advertisement, OfferManagement,UserPageInfo

# FastAPI uygulaması oluşturma
app = FastAPI()

# Router'ları uygulamaya dahil etme
app.include_router(Authentication.router)
app.include_router(Advertisement.router)
app.include_router(OfferManagement.router)
app.include_router(UserPageInfo.router)

@app.get("/ping")
async def root():
    return {"message": "Welcome to the Beeroomie application!"}

# Eğer direkt Python dosyasını çalıştırıyorsanız
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)