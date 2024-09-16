"""
This module is used to manage and connect to the database.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __table_args__ = {
        'extend_existing': True
    }


engine = create_async_engine("postgresql+asyncpg://gen_user:r%7C%5Equ%26n%3EZ.72oQ@192.168.0.6:5432/default_db")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

