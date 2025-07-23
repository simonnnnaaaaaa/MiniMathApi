from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from app.services import pow_int, fib, fact
from app.db       import init_db, get_session
from app.models   import RequestLog

init_db()
print("✅ init_db() called, DB ready")
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
@app.get("/")
def read_root():
    print("🔍 DEBUG: read_root was called")
    return {"message": "Hello from FastAPI 👋"}



@app.post("/pow", response_model=PowResponse)
def calc_pow(
    body: PowRequest,
    session: Session = Depends(get_session),
):
    value = pow_int(body.x, body.y)

    log = RequestLog(
        operation="pow",
        input_json=body.model_dump_json(),
        result=str(value),
    )
    session.add(log)
    session.commit()

    return PowResponse(result=value)


@app.get("/fib/{n}", response_model=FibResponse)
def calc_fib(
    n: int,
    session: Session = Depends(get_session),
):
    # validare simplă
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be >= 0")

    # 1) calcul
    value = fib(n)

    print(f"DEBUG fib called: n={n}, value={value}")

    # 2) log
    log = RequestLog(
        operation="fib",
        input_json=str(n),
        result=str(value),
    )
    session.add(log)
    session.commit()

    # 3) răspuns
    return FibResponse(result=value)


@app.get("/fact/{n}", response_model=FactResponse)
def calc_fact(
    n: int,
    session: Session = Depends(get_session),
):
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be >= 0")

    value = fact(n)

    print(f"DEBUG fact(): called with n={n}, computed value={value}")

    log = RequestLog(
        operation="fact",
        input_json=str(n),
        result=str(value),
    )
    session.add(log)
    session.commit()

    return FactResponse(result=value)

