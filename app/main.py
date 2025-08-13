from fastapi import FastAPI, Depends
from app.db import init_db
from app.routers import math as math_router
from prometheus_fastapi_instrumentator import Instrumentator
from app.deps import verify_api_key

init_db()
app = FastAPI(title="Mini-Math API")

app.include_router(math_router.router)

Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False,
)

@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI 👋"}
