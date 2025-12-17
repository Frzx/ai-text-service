import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

load_dotenv()

# DATABASE CONFIGURATION
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB= os.getenv("POSTGRES_DB")
DIALECT = "postgresql+asyncpg"

POSTGRES_URL = (
            f"{DIALECT}://"
            f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
            f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# DATABASE ENGINE
engine = create_async_engine(
    url=POSTGRES_URL
)

# Sessionmaker
async_session = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

# session dependency
async def get_session():
    async with async_session() as session:
        yield session

# Session Dependency annotation
SessionDep = Annotated[AsyncSession,Depends(get_session)]


# function to create all the tables
async def create_all_tables():
    from app.model import Label, Sentiment  # noqa : F401
    async with engine.begin() as connection:
        await connection.run_sync(
            SQLModel.metadata.create_all
        )


