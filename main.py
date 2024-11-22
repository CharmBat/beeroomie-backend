from fastapi import FastAPI
from routers import Authentication

app = FastAPI()

app.include_router(Authentication.router)






