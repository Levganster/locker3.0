from fastapi import APIRouter, Depends, HTTPException,Security
from fastapi_jwt import JwtAuthorizationCredentials
from core.auth.views import access_security, admin_required

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

router.canAuth = False

@router.post('/disable')
async def set_auth(credentials: JwtAuthorizationCredentials = Depends(admin_required)):
    router.canAuth = False

@router.post('/enable')
async def set_auth(credentials: JwtAuthorizationCredentials = Depends(admin_required)):
    router.canAuth = True

@router.get('/get_authstate')
def get_authstate():
    return router.canAuth