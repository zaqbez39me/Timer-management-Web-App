import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from starlette.testclient import TestClient

from fastapi_app.api.settings import pg_test_settings
from fastapi_app.database import db_engine
from fastapi_app.database.models import Base
from fastapi_app.main import app

engine = create_async_engine(pg_test_settings.pg_database_uri)
session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
metadata = Base.metadata
metadata.bind = engine


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session

app.dependency_overrides[db_engine.session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    # Prepare all the tables in database
    # before testing
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    # Clear the database after testing
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    # Each test case will be provided with a single
    # event loop instance.
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client

