import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_KEY_HEADER_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

EXPECTED_API_KEY = os.getenv("API_KEY")

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    if not EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfigured: API key not set",
        )

    if not api_key or api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return api_key
