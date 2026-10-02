from fastapi import FastAPI
from database import engine, Base
from routers import admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookNook API", version="2.0")

app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "BookNook Sprint 2 API is running"}