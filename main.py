from fastapi import FastAPI
from routers import Authentication, Advertisement
app = FastAPI()

app.include_router(Authentication.router)
app.include_router(Advertisement.router)




