import pytest
import requests
from fastapi.testclient import TestClient

from fastapi_app.database.models.user import UserDB
from fastapi_app.database.utils import delete_by_model_value
from fastapi_app.api.settings import custom_db_settings
from fastapi_app.main import app
from fastapi_app.custom_database.utils import get_custom_db_worker, CustomDBWorker, get_connection
from tests.conftest import entity_name_to_create


# @pytest.mark.asyncio
# async def test_register_endpoint(db):
#     # Test case 1: Successful registration
#     payload = {"username": "testuser", "password": "testpassword"}
#     with TestClient(app) as client:
#         response = client.post("/auth/register", data=payload)
#     assert response.status_code == 201
#     assert "User Created Successfully" in response.json()["message"]
#
#     # Test case 2: Username already exists
#     payload = {"username": "testuser", "password": "testpassword"}
#     with TestClient(app) as client:
#         response = client.post("/auth/register", data=payload)
#     assert response.status_code == 409
#     assert "Username already in use." in response.json()["detail"]
#     await delete_by_model_value(await db, UserDB, UserDB.username, "testuser", commit=True)


@pytest.mark.asyncio
async def test_custom_bd(custom_db_worker):
    assert {'Error': f"'{entity_name_to_create}' is not defined"} == await custom_db_worker.send_only_query(f'get [{entity_name_to_create}]')

    await custom_db_worker.send_only_query(f'create entity {entity_name_to_create} {{}}')

    assert {'Ok': []} == await custom_db_worker.send_only_query(f'get [{entity_name_to_create}]')