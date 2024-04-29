import contextlib
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    def init(self, db_url: str) -> None:
        if "postgresql" in db_url:
            connect_args = {
                "statement_cache_size": 0,
                "prepared_statement_cache_size": 0,
            }
        else:
            connect_args = {}
        self._engine = create_async_engine(
            url=db_url,
            pool_pre_ping=True,
            connect_args=connect_args,
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise


db_manager = DatabaseSessionManager()

async def get_db() -> AsyncIterator[AsyncSession]:
    async with db_manager.session() as session:
        yield session
            
# from collections.abc import AsyncGenerator

# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import async_sessionmaker

# from app.config import POSTGRES_DATABASE_URL

# engine = create_async_engine(
#     POSTGRES_DATABASE_URL,
#     future=True,
#     echo=True,
# )

# # expire_on_commit=False will prevent attributes from being expired
# # after commit.
# AsyncSessionFactory = async_sessionmaker(
#     engine,
#     autoflush=False,
#     expire_on_commit=False,
# )


# # Dependency
# async def get_db() -> AsyncGenerator:
#     async with AsyncSessionFactory() as session:
#         # logger.debug(f"ASYNC Pool: {engine.pool.status()}")
#         yield session
