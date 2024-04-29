import pytest
from fastapi import status
from httpx import AsyncClient
from tests.utils import create_driver
import copy

DEFAULT_DRIVER = {
    "last_name": "Last name",
    "first_name": "First name",
    "patronymic": "Patronymic",
    "passport": "0480614017",
    "experience": "2024-03-03"
}

async def test_create_driver(client: AsyncClient):
    response = await client.post("/api/drivers", json = DEFAULT_DRIVER)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()["driver_id"]) is int

async def test_create_driver_uprocessable_entity(client: AsyncClient):
    create_driver = copy.deepcopy(DEFAULT_DRIVER)

    create_driver["first_name"] = ""

    response = await client.post("/api/drivers", json = create_driver)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_get_driver(client: AsyncClient):
    driver_id = await create_driver(client, DEFAULT_DRIVER)

    response = await client.get(f"/api/drivers/{driver_id}")
    assert response.status_code == status.HTTP_200_OK

    response = response.json()    
    assert DEFAULT_DRIVER["first_name"] == response["first_name"]
    assert DEFAULT_DRIVER["passport"] == response["passport"]
    assert DEFAULT_DRIVER["last_name"] == response["last_name"]
    assert DEFAULT_DRIVER["patronymic"] == response["patronymic"]
    assert DEFAULT_DRIVER["experience"] == response["experience"]

async def test_get_driver_not_found(client: AsyncClient):
    response = await client.get(f"/api/drivers/1239035234")
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_get_drivers(client: AsyncClient):
    response = await client.get(f"/api/drivers")
    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    for driver in response:
        assert DEFAULT_DRIVER["first_name"] == driver["first_name"]
        assert DEFAULT_DRIVER["passport"] == driver["passport"]
        assert DEFAULT_DRIVER["last_name"] == driver["last_name"]
        assert DEFAULT_DRIVER["patronymic"] == driver["patronymic"]
        assert DEFAULT_DRIVER["experience"] == driver["experience"]

async def test_update_driver(client: AsyncClient):
    driver_id = await create_driver(client, DEFAULT_DRIVER)

    update_driver = copy.deepcopy(DEFAULT_DRIVER)
    update_driver["id"] = driver_id
    update_driver["first_name"] = "update first name"
    update_driver["last_name"] = "update last name"

    response = await client.put(f"/api/drivers", json = update_driver)
    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    assert update_driver["first_name"] == response["first_name"]
    assert DEFAULT_DRIVER["passport"] == response["passport"]
    assert update_driver["last_name"] == response["last_name"]
    assert DEFAULT_DRIVER["patronymic"] == response["patronymic"]
    assert DEFAULT_DRIVER["experience"] == response["experience"]

async def test_update_driver_not_found(client: AsyncClient):
    update_driver = copy.deepcopy(DEFAULT_DRIVER)
    update_driver["id"] = 2346332

    response = await client.put(f"/api/drivers", json = update_driver)
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_update_driver_unprocessable_entity(client: AsyncClient):
    driver_id = await create_driver(client, DEFAULT_DRIVER)

    update_driver = copy.deepcopy(DEFAULT_DRIVER)
    update_driver["id"] = driver_id
    update_driver["first_name"] = ""
    update_driver["last_name"] = ""

    response = await client.put(f"/api/drivers", json = update_driver)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_patch_driver(client: AsyncClient):
    driver_id = await create_driver(client, DEFAULT_DRIVER)

    update_driver = {
        "id": driver_id,
        "last_name": "patch last name"
    }

    response = await client.patch(f"/api/drivers", json = update_driver)
    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    assert DEFAULT_DRIVER["first_name"] == response["first_name"]
    assert DEFAULT_DRIVER["passport"] == response["passport"]
    assert update_driver["last_name"] == response["last_name"]
    assert DEFAULT_DRIVER["patronymic"] == response["patronymic"]
    assert DEFAULT_DRIVER["experience"] == response["experience"]

async def test_patch_driver_not_found(client: AsyncClient):
    update_driver = {"id": 2346332}

    response = await client.patch(f"/api/drivers", json = update_driver)
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_patch_driver_unprocessable_entity(client: AsyncClient):
    driver_id = await create_driver(client, DEFAULT_DRIVER)

    update_driver = {
        "id": driver_id,
        "last_name": ""
    }

    response = await client.patch(f"/api/drivers", json = update_driver)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_delete_driver(client: AsyncClient):    
    driver_id = await create_driver(client, DEFAULT_DRIVER)

    response = await client.delete(f"/api/drivers/{driver_id}")
    assert response.status_code == status.HTTP_200_OK

async def test_delete_driver_not_found(client: AsyncClient):
    response = await client.delete(f"/api/drivers/1239035234")
    assert response.status_code == status.HTTP_404_NOT_FOUND