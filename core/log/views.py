from fastapi import APIRouter, HTTPException,Security
from fastapi_jwt import JwtAuthorizationCredentials
from core.auth.views import access_security
from core.log.logger import get_logs_as_json

from core.log.config import (
    PREFIX,
    TAGS,
    INCLUDE_IN_SCHEMA
)

router = APIRouter(
    prefix=PREFIX,
    tags=TAGS,
    include_in_schema=INCLUDE_IN_SCHEMA
)

@router.get('/get_logs')
async def get_logs(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials["admin"]:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    return get_logs_as_json()