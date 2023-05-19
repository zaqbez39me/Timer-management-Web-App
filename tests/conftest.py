import pytest

from fastapi_app.database import DatabaseEngine

from fastapi_app.api import pg_settings
from fastapi_app.custom_database.utils import get_custom_db_worker, CustomDBWorker, get_connection
db_engine = DatabaseEngine(pg_settings.pg_database_uri)


@pytest.fixture(scope="session")
async def db():
    return await anext(db_engine.session())


entity_name_to_create = "some_unknown_and_unusable_entity"


@pytest.mark.asyncio
@pytest.fixture
async def custom_db_worker():
    worker = get_custom_db_worker(CustomDBWorker)(next(get_connection()))

    yield worker

    await worker.send_only_query(f'drop entity {entity_name_to_create} {{}}')
