from .models import User
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .base import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/ganeshaidol"


engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as session:
        yield session

async def insert_user(user:dict):
    async for session in get_db():

        db_user = User(**user)
        session.add(db_user)
        await session.commit()
        return db_user


