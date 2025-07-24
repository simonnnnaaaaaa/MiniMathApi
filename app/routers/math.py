# app/routers/math.py
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.services import pow_int, fib, fact
from app.db import get_session
from app.models import RequestLog
from concurrent.futures import ThreadPoolExecutor
import asyncio

executor = ThreadPoolExecutor(max_workers=5)

router = APIRouter(tags=["math"])  # „/” prefix implicit


# --------- modele Pydantic -------------
class PowRequest(BaseModel):
    x: int
    y: int


class PowResponse(BaseModel):
    result: int


class FibResponse(BaseModel):
    result: int


class FactResponse(BaseModel):
    result: int


class LogEntry(BaseModel):
    id: int
    operation: str
    input_json: str
    result: str
    ts: datetime


# --------- endpoint‑uri -----------------


@router.post("/pow", response_model=PowResponse)
async def calc_pow(body: PowRequest, session: Session = Depends(get_session)):
    loop = asyncio.get_running_loop()
    value = await loop.run_in_executor(executor, pow_int, body.x, body.y)

    log = RequestLog(
        operation="pow", input_json=body.model_dump_json(), result=str(value)
    )
    session.add(log)
    session.commit()

    return PowResponse(result=value)


@router.get("/fib/{n}", response_model=FibResponse)
async def calc_fib(n: int, session: Session = Depends(get_session)):
    loop = asyncio.get_running_loop()
    value = await loop.run_in_executor(executor, fib, n)

    log = RequestLog(operation="fib", input_json=str(n), result=str(value))
    session.add(log)
    session.commit()

    return FibResponse(result=value)


@router.get("/fact/{n}", response_model=FactResponse)
async def calc_fact(n: int, session: Session = Depends(get_session)):
    loop = asyncio.get_running_loop()
    value = await loop.run_in_executor(executor, fact, n)

    log = RequestLog(operation="fact", input_json=str(n), result=str(value))
    session.add(log)
    session.commit()

    return FactResponse(result=value)


@router.get("/history", response_model=List[LogEntry])
def get_history(
    page: int = 1,
    size: int = 50,
    session: Session = Depends(get_session),
):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="page/size must be >= 1")

    offset = (page - 1) * size
    rows = (
        session.query(RequestLog)
        .order_by(RequestLog.id.desc())
        .offset(offset)
        .limit(size)
        .all()
    )
    return rows
