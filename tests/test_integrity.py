import pytest
from httpx import AsyncClient

from tests.conftest import (async_client, 
                            entity_name_to_create, session_maker)


async def test_register_endpoint(async_client: AsyncClient):
    # Test case 1: Successful registration
    payload = {"username": "testuser", "password": "testpassword"}
    response = await async_client.post("/auth/register", data=payload)
    assert response.status_code == 201
    assert "User Created Successfully" in response.json()["message"]


async def test_register_user_already_exists(async_client: AsyncClient):
    # Test case 2: Username already exists
    payload = {"username": "testuser", "password": "testpassword"}
    response = await async_client.post("/auth/register", data=payload)
    assert response.status_code == 409
    assert "Username already in use." in response.json()["detail"]


async def test_custom_bd(custom_db_worker):
    assert {'Error': f"'{entity_name_to_create}' is not defined"} == await \
        custom_db_worker.send_only_query(f'get [{entity_name_to_create}]')

    await custom_db_worker.send_only_query(f'create entity {entity_name_to_create} {{}}')

    assert {'Ok': []} == await custom_db_worker.send_only_query(f'get [{entity_name_to_create}]')