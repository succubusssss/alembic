import pytest
from fastapi import status
from httpx import AsyncClient
from tests.utils import create_user
import copy

DEFAULT_USER = {
    "first_name": "Фамилия",
    "group": "Группа",
    "last_name": "Имя",
    "patronymic": "Отчество"
}

async def test_create_user(client: AsyncClient):
    response = await client.post("/api/users", json = DEFAULT_USER)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()["user_id"]) is int

async def test_create_user_uprocessable_entity(client: AsyncClient):
    create_user = copy.deepcopy(DEFAULT_USER)

    create_user["first_name"] = ""

    response = await client.post("/api/users", json = create_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_get_user(client: AsyncClient):
    user_id = await create_user(client, DEFAULT_USER)

    response = await client.get(f"/api/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK

    response = response.json()    
    assert DEFAULT_USER["first_name"] == response["first_name"]
    assert DEFAULT_USER["group"] == response["group"]
    assert DEFAULT_USER["last_name"] == response["last_name"]
    assert DEFAULT_USER["patronymic"] == response["patronymic"]

async def test_get_user_not_found(client: AsyncClient):
    response = await client.get(f"/api/users/1239035234")
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_get_users(client: AsyncClient):
    response = await client.get(f"/api/users")
    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    for user in response:
        assert DEFAULT_USER["first_name"] == user["first_name"]
        assert DEFAULT_USER["group"] == user["group"]
        assert DEFAULT_USER["last_name"] == user["last_name"]
        assert DEFAULT_USER["patronymic"] == user["patronymic"]

async def test_update_user(client: AsyncClient):
    user_id = await create_user(client, DEFAULT_USER)

    update_user = copy.deepcopy(DEFAULT_USER)
    update_user["id"] = user_id
    update_user["first_name"] = "update first name"
    update_user["last_name"] = "update last name"

    response = await client.put(f"/api/users", json = update_user)
    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    assert update_user["first_name"] == response["first_name"]
    assert DEFAULT_USER["group"] == response["group"]
    assert update_user["last_name"] == response["last_name"]
    assert DEFAULT_USER["patronymic"] == response["patronymic"]

async def test_update_user_not_found(client: AsyncClient):
    update_user = copy.deepcopy(DEFAULT_USER)
    update_user["id"] = 2346332

    response = await client.put(f"/api/users", json = update_user)
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_update_user_unprocessable_entity(client: AsyncClient):
    user_id = await create_user(client, DEFAULT_USER)

    update_user = copy.deepcopy(DEFAULT_USER)
    update_user["id"] = user_id
    update_user["first_name"] = ""
    update_user["last_name"] = ""

    response = await client.put(f"/api/users", json = update_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_patch_user(client: AsyncClient):
    user_id = await create_user(client, DEFAULT_USER)

    update_user = {
        "id": user_id,
        "last_name": "patch last name"
    }

    response = await client.patch(f"/api/users", json = update_user)
    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    assert DEFAULT_USER["first_name"] == response["first_name"]
    assert DEFAULT_USER["group"] == response["group"]
    assert update_user["last_name"] == response["last_name"]
    assert DEFAULT_USER["patronymic"] == response["patronymic"]

async def test_patch_user_not_found(client: AsyncClient):
    update_user = {"id": 2346332}

    response = await client.patch(f"/api/users", json = update_user)
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_patch_user_unprocessable_entity(client: AsyncClient):
    user_id = await create_user(client, DEFAULT_USER)

    update_user = {
        "id": user_id,
        "last_name": ""
    }

    response = await client.patch(f"/api/users", json = update_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_delete_user(client: AsyncClient):    
    user_id = await create_user(client, DEFAULT_USER)

    response = await client.delete(f"/api/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK

async def test_delete_user_not_found(client: AsyncClient):
    response = await client.delete(f"/api/users/1239035234")
    assert response.status_code == status.HTTP_404_NOT_FOUND