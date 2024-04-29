import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import BaseModel
from app.config import POSTGRES_TEST_DATABASE_URL

from tests.db_utils import alembic_config_from_url

@pytest.fixture()
async def postgres_engine():
    engine = create_async_engine(
        url=POSTGRES_TEST_DATABASE_URL,
        pool_pre_ping=True,
    )
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture()
def alembic_config():
    return alembic_config_from_url(POSTGRES_TEST_DATABASE_URL)
