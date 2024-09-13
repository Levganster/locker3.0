"""
This class is used to interact with the database.
You can create your own or use it as a base class.
"""

from abc import ABC, abstractmethod
from sqlalchemy import delete, insert, select, and_, update

from core.database import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def create():
        raise NotImplementedError

    @abstractmethod
    async def read_all():
        raise NotImplementedError

    @abstractmethod
    async def read_by_id():
        raise NotImplementedError

    @abstractmethod
    async def read_by_data():
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id():
        raise NotImplementedError
    
    @abstractmethod
    async def update_by_id():
        raise NotImplementedError
    


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def create(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(statement=stmt)
            await session.flush()
            await session.commit()
            return res.scalar_one()

    async def read_all(self, limit: int, offset: int):
        async with async_session_maker() as session:
            stmt = select(self.model).limit(limit).offset(offset)
            res = await session.execute(statement=stmt)
            return res.scalars().all()

    async def read_by_id(self, id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(id=id)
            res = await session.execute(statement=stmt)
            return res.scalar()

    async def read_by_data(self, **filters):
        async with async_session_maker() as session:
            stmt = select(self.model).where(
                and_(
                    *[
                        getattr(self.model, key) == value for key, value in filters.items()
                    ]
                )
            )
            res = await session.execute(stmt)
            return res.scalar()

    async def delete_by_id(self, id: int):
        async with async_session_maker() as session:
            stmt = delete(self.model).filter_by(id=id).returning(self.model)
            res = await session.execute(statement=stmt)
            await session.commit()
            return res.scalar()
        
    async def update_by_id(self, id: int, new_data: dict):
        async with async_session_maker() as session:
            stmt = update(self.model).where(
                id==id
            ).values(new_data).returning(self.model)
            
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()
     
        
    