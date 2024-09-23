"""
Views controllers for user app
"""


from fastapi import APIRouter, HTTPException, status, Depends, Security

from core.user.config import (
    PREFIX,
    TAGS,
    INCLUDE_IN_SCHEMA
)

from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials

from core.user.dependencies import get_user_service
from core.user.service import UserService
from core.user.schemas import UserCreateSchema, UserGetSchema

from core.auth.views import access_security


router = APIRouter(
    prefix=PREFIX,
    tags=TAGS,
    include_in_schema=INCLUDE_IN_SCHEMA
)


@router.get('/{id}', response_model=UserGetSchema, status_code=status.HTTP_200_OK)
async def get_one(
    id: int,
    credentials: JwtAuthorizationCredentials = Security(access_security),
    service: UserService = Depends(get_user_service),
):
    if not credentials["admin"] and credentials:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    item = await service.get_by_id(id)
    return item


@router.post('/', response_model=UserGetSchema, status_code=status.HTTP_201_CREATED)
async def create_one(
    item: UserCreateSchema,
    credentials: JwtAuthorizationCredentials = Security(access_security),
    service: UserService = Depends(get_user_service),
):
    if not credentials["admin"] and credentials:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    new_item = await service.create(item)
    return new_item


@router.put('/{id}', response_model=UserGetSchema, status_code=status.HTTP_200_OK)
async def update_one(
    id: int,
    new_item: UserCreateSchema,
    credentials: JwtAuthorizationCredentials = Security(access_security),
    service: UserService = Depends(get_user_service),
):
    if not credentials["admin"] and credentials:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    new_item = await service.update(id, new_item)
    return new_item


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_one(
    id: int,
    credentials: JwtAuthorizationCredentials = Security(access_security),
    service: UserService = Depends(get_user_service),
):
    if not credentials["admin"] and credentials:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    await service.delete(id)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    limit: int = 10,
    offset: int = 0,
    service: UserService = Depends(get_user_service),
):
    if not credentials["admin"] and credentials:
        raise HTTPException(status_code=403, detail="You dont have permission to access")
    items = await service.get_all(limit=limit, offset=offset)
    return items