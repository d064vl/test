import databases
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_scoped_session
)

# metadata (Objs to create on the DB)
# metadata = sqlalchemy.MetaData()

from sqlalchemy.orm import DeclarativeBase

from asyncio import current_task

###
###

# Get .env data
from storeapi.DB.config import config
from storeapi.schemas.Base import Base


###########################
###########################


database = databases.Database(
    config.DATABASE_URL, 
    force_rollback=config.DB_FORCE_ROLL_BACK
)

async_engine = create_async_engine(
    config.DATABASE_URL, 
)

# Session
async_session = async_sessionmaker(
                                bind=async_engine,
                                expire_on_commit=False
                                )

# Scope-Session
async_session_scope = async_scoped_session(
                                            session_factory=async_session, 
                                            scopefunc=current_task
                                        )

# Get Scope-Session
async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """Get a database session.
    To be used for dependency injection.
    """
    async with async_session_scope() as session, session.begin():
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()



async def init_models() -> None:
    """Create tables if they don't already exist.
    In a real-life example we would use Alembic to manage migrations.
    """
    async with async_engine.begin() as conn:
        print(Base.metadata.create_all)
        await conn.run_sync(Base.metadata.create_all)

# Close DB
async def close():
    await async_engine.dispose()




