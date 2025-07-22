from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.services import pow_int
from app.services import pow_int, fib
from app.services import pow_int, fib, fact

from app.db import  get_session
from sqlmodel import Session
from app.models import RequestLog



from app.db import init_db
init_db()

app = FastAPI(title="Mini-Math API")

# --- MODELE -------------------------------------------------
class PowRequest(BaseModel):
    x: int
    y: int

class PowResponse(BaseModel):
    result: int

class FibResponse(BaseModel):
    result: int

class FactResponse(BaseModel):
    result: int

# --- ENDPOINTS ------------------------------------------------
#@app.post("/pow", response_model=PowResponse)
# def calc_pow(body: PowRequest):
#     value = pow_int(body.x, body.y)
#     return PowResponse(result=value)

@app.post("/pow", response_model=PowResponse)
def calc_pow(
    body: PowRequest,
    session: Session = Depends(get_session)
):
    value = pow_int(body.x, body.y)

    # --- logăm cererea în SQLite -------------------------
    log = RequestLog(
        operation="pow",
        input_json=body.model_dump_json(),
        result=str(value)
    )
    session.add(log)
    session.commit()
    # -----------------------------------------------------

    return PowResponse(result=value)




@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI 👋"}

@app.get("/fib/{n}", response_model=FibResponse)
def calc_fib(n: int):
    """
    Returnează F(n) (0-based): F(0)=0, F(1)=1…
    Restricționează n la interval rezonabil (ex: 0-9 999) dacă vrei.
    """
    value = fib(n)
    return FibResponse(result=value)

@app.get("/fact/{n}", response_model=FactResponse)
def calc_fact(n: int):
    value = fact(n)
    return FactResponse(result=value)
