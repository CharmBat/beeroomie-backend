from fastapi import FastAPI
from routers import Authentication, Advertisement, OfferManagement,UserPageInfo, Administration
from routers import Authentication, Advertisement, OfferManagement,UserPageInfo, favorites,PhotoHandle
from fastapi.middleware.cors import CORSMiddleware
from config import FRONTEND_URL_PREFIX

origins = [

    FRONTEND_URL_PREFIX,

]
# FastAPI uygulaması oluşturma
app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# Router'ları uygulamaya dahil etme
app.include_router(Authentication.router)
app.include_router(Advertisement.router)
app.include_router(OfferManagement.router)
app.include_router(UserPageInfo.router)
app.include_router(Administration.router)
app.include_router(favorites.router)
app.include_router(PhotoHandle.router)


@app.get("/ping")
async def root():
    return {"message": "Welcome to the Beeroomie application!"}

# Eğer direkt Python dosyasını çalıştırıyorsanız
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)