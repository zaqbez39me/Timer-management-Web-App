from datetime import datetime

from httpx import AsyncClient

from tests.conftest import (async_client, 
                            entity_name_to_create, session_maker)

cookies = None
tokens = None


async def test_register_endpoint(async_client: AsyncClient):
    # Test case 1: Successful registration
    payload = {"username": "testuser", "password": "testpassword"}
    response = await async_client.post("/auth/register", data=payload)
    assert response.status_code == 201, "Incorrect success status code"
    assert "User Created Successfully" in response.json()["message"], \
        "Incorrect successful registration message"

    # Test case 2: Username already exists
    response = await async_client.post("/auth/register", data=payload)
    assert response.status_code == 409, "Incorrect registration failure status code"
    assert "Username already in use." in response.json()["detail"], \
        "Incorrect detail for registration failure"


async def test_login(async_client: AsyncClient):
    global cookies, tokens
    # Test case 1: Login successfully
    payload = {"username": "testuser", "password": "testpassword"}
    response = await async_client.post("/auth/login", data=payload)
    assert response.status_code == 200, \
        "Incorrect status code for successful authorization"
    assert response.json()["access_token"] is not None, \
        "Access token is missing"
    assert response.json()["refresh_token"] is not None, \
        "Refresh token is missing"
    assert response.json()["token_type"] == "bearer", \
        "Incorrect authorization type"
    assert response.json()["data"]["username"] == payload["username"], \
        "Incorrect username value from authorization"
    assert "User Logged in successfully." in response.json()["message"], \
        "Incorrect message from authorization"
    cookies = response.cookies
    tokens = {
        "access_token": response.json()["access_token"],
        "refresh_token": response.json()["refresh_token"]
    }

    # Test case 2: Wrong password
    payload = {"username": "testuser", "password": "wrongtestpassword"}
    response = await async_client.post("/auth/login", data=payload)
    assert response.status_code == 401, \
        "Incorrect status code for authorization failure"
    assert "Incorrect username or password." in response.json()["detail"], \
        "Incorrect message for authorization failure"


async def test_get_user_me(async_client: AsyncClient):
    global cookies, tokens
    # Test case 1: Get user me successfully
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = await async_client.get("/auth/user/me", cookies=cookies, headers=headers)
    assert response.status_code == 200, \
        "Incorrect status code for get me user success"
    assert "User information report." in response.json()["message"], \
        "Incorrect message for get me user success"
    assert "user" in response.json(), \
        "No user info in get me user successful response"

    # Test case 2: No authentication
    response = await async_client.get("/auth/user/me", cookies=cookies)
    assert response.status_code == 401, \
        "Incorrect status code for no authentication headers case in get user me"
    assert "Not authenticated" in response.json()["detail"], \
        "Incorrect detail for no authentication headers case in get user"


async def test_get_server_time(async_client: AsyncClient):
    global cookies, tokens
    # Test case 1: Get server time successfully
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = await async_client.get("/time_sync", cookies=cookies, headers=headers)
    assert response.status_code == 200, "Incorrect status code for get server time success"
    try:
        server_time = datetime.fromisoformat(
            response.json()["server_time"])
    except ValueError:
        raise ValueError("Incorrect response time in get server time success")

    # Test case 2: No authentication
    response = await async_client.get("/time_sync", cookies=cookies)
    assert response.status_code == 401, \
        "Incorrect status code for no authentication headers case in time sync"
    assert "Not authenticated" in response.json()["detail"], \
        "Incorrect detail for no authentication headers case in time sync"


async def test_custom_bd(custom_db_worker):
    assert {'Error': f"'{entity_name_to_create}' is not defined"} == await \
        custom_db_worker.send_only_query(f'get [{entity_name_to_create}]')

    await custom_db_worker.send_only_query(f'create entity {entity_name_to_create} {{}}')

    assert {'Ok': []} == await custom_db_worker.send_only_query(f'get [{entity_name_to_create}]')
