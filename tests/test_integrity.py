import pytest
from fastapi.testclient import TestClient

from fastapi_app.database.models.user import UserDB
from fastapi_app.database.utils import delete_by_model_value

from fastapi_app.main import app


@pytest.mark.asyncio
async def test_register_endpoint(db):
    # Test case 1: Successful registration
    payload = {"username": "testuser", "password": "testpassword"}
    with TestClient(app) as client:
        response = client.post("/auth/register", data=payload)
    assert response.status_code == 201
    assert "User Created Successfully" in response.json()["message"]

    # Test case 2: Username already exists
    payload = {"username": "testuser", "password": "testpassword"}
    with TestClient(app) as client:
        response = client.post("/auth/register", data=payload)
    assert response.status_code == 409
    assert "Username already in use." in response.json()["detail"]
    await delete_by_model_value(await db, UserDB, UserDB.username, "testuser", commit=True)
