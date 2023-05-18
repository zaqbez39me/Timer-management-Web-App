import pytest

from fastapi_app.database import DatabaseEngine

from fastapi_app.api import pg_settings

db_engine = DatabaseEngine(pg_settings.pg_database_uri)


@pytest.fixture(scope="session")
async def db():
    return await anext(db_engine.session())
