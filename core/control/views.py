from fastapi import APIRouter, HTTPException,Security
from fastapi_jwt import JwtAuthorizationCredentials
from core.auth.views import access_security

from core.control.config import (
    PREFIX,
    TAGS,
    INCLUDE_IN_SCHEMA
)

router = APIRouter(
    prefix=PREFIX,
    tags=TAGS,
    include_in_schema=INCLUDE_IN_SCHEMA
)


canAuth = False

@router.post('/disable')
async def set_auth(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials["admin"]:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    global canAuth
    canAuth = False

@router.post('/enable')
async def set_auth(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials["admin"]:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    global canAuth
    canAuth = True

@router.get('/get_authstate')
def get_authstate():
    global canAuth
    return(canAuth)