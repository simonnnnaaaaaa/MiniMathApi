from fastapi import FastAPI, Depends
from app.db import init_db
from app.routers import math as math_router
from prometheus_fastapi_instrumentator import Instrumentator
from app.deps import verify_api_key

init_db()
app = FastAPI(title="Mini-Math API", dependencies=[Depends(verify_api_key)])

app.include_router(math_router.router)
Instrumentator().instrument(app).expose(app)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI 👋"}
