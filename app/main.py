# app/main.py
from fastapi import FastAPI
from app.db import init_db
from app.routers import math as math_router  # <— noul import
from prometheus_fastapi_instrumentator import Instrumentator

init_db()
app = FastAPI(title="Mini-Math API")

app.include_router(math_router.router)  # <— montăm toate rutele
Instrumentator().instrument(app).expose(app)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI 👋"}
