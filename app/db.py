import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# DATABASE CONFIGURATION
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGERS_PORT = os.getenv("POSTGERS_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB= os.getenv("POSTGRES_DB")
DIALECT = "postgresql+asyncpg"

POSTGRES_URL = (
            f"{DIALECT}://"
            f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
            f"{POSTGRES_SERVER}:{POSTGRES_PASSWORD}/{POSTGRES_DB}"
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


