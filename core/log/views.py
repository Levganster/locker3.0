from fastapi import APIRouter, Depends, HTTPException,Security
from fastapi_jwt import JwtAuthorizationCredentials
from core.auth.views import access_security, admin_required
from core.log.logger import read_logs, delete_logs, log_event

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
async def get_logs(credentials: JwtAuthorizationCredentials = Depends(admin_required)):
    return read_logs()

@router.post('/delete_logs')
async def delete_amount_of_logs(credentials: JwtAuthorizationCredentials = Depends(admin_required),amount: int = 0):
    delete_logs(amount)