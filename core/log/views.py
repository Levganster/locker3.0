from fastapi import APIRouter, HTTPException,Security
from fastapi_jwt import JwtAuthorizationCredentials
from core.auth.views import access_security
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
async def get_logs(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials["admin"] and credentials:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    return read_logs()

@router.post('/delete_logs')
async def delete_amount_of_logs(credentials: JwtAuthorizationCredentials = Security(access_security),amount: int = 0):
    if not credentials["admin"] and credentials:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    delete_logs(amount)

@router.post('/send_log')
async def send_log(event: str,id: str, username: str, group: str):
    log_event(id, event, username, group)