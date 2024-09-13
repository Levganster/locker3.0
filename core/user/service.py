"""
user app service and repository
"""

from sqlalchemy.exc import IntegrityError

from core.abstract_repository import SQLAlchemyRepository, AbstractRepository
from core.user.models import User
from core.exceptions import ConflictException, NotFoundException
from core.user.schemas import UserCreateSchema

# TODO: define your service here and rename if it's necessary
# WARNING: if this sevice doesn't work with DB,
# you may implement only your own service
# TODO: rename YourModel to name of your model with press F2 button on class name


class UserRepository(SQLAlchemyRepository):
    model = User


class UserService:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def create(self, item: UserCreateSchema):
        item_dict = item.model_dump()
        try:
            return await self.repository.create(item_dict)
        except IntegrityError:
            raise ConflictException()

    async def get_all(self, limit: int, offset: int):
        if items := await self.repository.read_all(limit, offset):
            return items
        raise NotFoundException()

    async def get_by_id(self, id: int):
        if item := await self.repository.read_by_id(id):
            return item
        raise NotFoundException()

    async def update(self, id: int, item: UserCreateSchema):
        item_dict = item.model_dump()
    
        if upd_item := await self.repository.update_by_id(id, item_dict):
            return upd_item
        raise NotFoundException()

    async def delete(self, id: int):
        if item := await self.repository.delete_by_id(id):
            return item
        raise NotFoundException()