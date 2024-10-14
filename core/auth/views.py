"""
Views controllers for auth app
"""

from datetime import timedelta
from fastapi import APIRouter, Response, Depends, HTTPException, Security
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.auth.schemas import AuthCreateSchema
from fastapi_jwt import JwtAccessBearerCookie, JwtAuthorizationCredentials
from core.auth.schemas import AuthCreateSchema
from core.database import get_async_session
from core.user.models import User

access_security = JwtAccessBearerCookie(secret_key="secret_key", auto_error=True, access_expires_delta=timedelta(days=7))

from core.control.views import get_authstate

from core.auth.config import (
    PREFIX,
    TAGS,
    INCLUDE_IN_SCHEMA
)

router = APIRouter(
    prefix=PREFIX,
    tags=TAGS,
    include_in_schema=INCLUDE_IN_SCHEMA
)

@router.post("/token")
async def auth(user: AuthCreateSchema, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.username == user.username))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=422, detail="Invalid username or password")

    if not get_authstate() and not db_user.admin:
        raise HTTPException(status_code=400, detail="Cant auth now")
    
    if user.password != db_user.password:
        raise HTTPException(status_code=422, detail="Invalid username or password")
    subject = {'username': db_user.username, 'admin': db_user.admin, 'group': db_user.group}
    return {"access_token": access_security.create_access_token(subject=subject)}

@router.post("/cookie")
async def auth(response: Response, user: AuthCreateSchema, session: AsyncSession = Depends(get_async_session)):


    result = await session.execute(select(User).where(User.username == user.username))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=422, detail="Invalid username or password")

    if not get_authstate() and not db_user.admin:
        raise HTTPException(status_code=400, detail="Cant auth now")

    if user.password != db_user.password:
        raise HTTPException(status_code=422, detail="Invalid username or password")
    subject = {'username': db_user.username, 'admin': db_user.admin, 'group': db_user.group}
    access_token = access_security.create_access_token(subject=subject)
    access_security.set_access_cookie(response, access_token)
    return {"access_token": access_token}


def admin_required(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials["admin"] and credentials:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    return credentials
