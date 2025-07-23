# app/main.py
from fastapi import FastAPI
from app.db import init_db
from app.routers import math as math_router  # <— noul import

init_db()
app = FastAPI(title="Mini-Math API")

app.include_router(math_router.router)       # <— montăm toate rutele

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI 👋"}
