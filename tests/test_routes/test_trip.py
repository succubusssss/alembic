import pytest
from fastapi import status
from httpx import AsyncClient
from tests.utils import create_trip, create_driver
from tests.test_routes.test_driver import DEFAULT_DRIVER
import copy

DEFAULT_TRIP = {
    "driver_id": 0,
    "departure_time": "2024-03-03T15:49:29"
}

async def test_create_trip(client: AsyncClient):
    driver_id = await create_driver(client, DEFAULT_DRIVER)

    trip = copy.deepcopy(DEFAULT_TRIP)
    trip["driver_id"] = driver_id
    response = await client.post("/api/trips", json = trip)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()["trip_id"]) is int

async def test_create_trip_uprocessable_entity(client: AsyncClient):
    trip = copy.deepcopy(DEFAULT_TRIP)

    trip["departure_time"] = ""

    response = await client.post("/api/trips", json = trip)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_get_trip(client: AsyncClient):
    driver_id = await create_driver(client, DEFAULT_DRIVER)
    trip = copy.deepcopy(DEFAULT_TRIP)
    trip["driver_id"] = driver_id
    trip_id = await create_trip(client, trip)

    response = await client.get(f"/api/trips/{trip_id}")
    assert response.status_code == status.HTTP_200_OK

    response = response.json()    
    assert DEFAULT_TRIP["departure_time"] == response["departure_time"]
    assert trip["driver_id"] == response["driver_id"]

async def test_get_trip_not_found(client: AsyncClient):
    response = await client.get(f"/api/trips/1239035234")
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_get_trips(client: AsyncClient):
    response = await client.get(f"/api/trips")
    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    for trip in response:
        assert DEFAULT_TRIP["departure_time"] == trip["departure_time"]

async def test_update_trip(client: AsyncClient):
    driver_id = await create_driver(client, DEFAULT_DRIVER)
    trip = copy.deepcopy(DEFAULT_TRIP)
    trip["driver_id"] = driver_id
    trip_id = await create_trip(client, trip)

    trip["id"] = trip_id
    trip["departure_time"] = "2024-01-04T15:49:29"

    response = await client.put(f"/api/trips", json = trip)
    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    assert response["departure_time"] == trip["departure_time"]

async def test_update_trip_not_found(client: AsyncClient):
    trip = copy.deepcopy(DEFAULT_TRIP)
    trip["id"] = 2346332
    trip["driver_id"] = 123

    response = await client.put(f"/api/trips", json = trip)
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_update_trip_unprocessable_entity(client: AsyncClient):
    response = await client.put(f"/api/trips", json = DEFAULT_TRIP)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_patch_trip(client: AsyncClient):
    driver_id = await create_driver(client, DEFAULT_DRIVER)
    trip = copy.deepcopy(DEFAULT_TRIP)
    trip["driver_id"] = driver_id
    trip_id = await create_trip(client, trip)

    trip["id"] = trip_id
    trip["departure_time"] = "2024-01-04T15:49:29"

    response = await client.patch(f"/api/trips", json = trip)
    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    assert response["departure_time"] == trip["departure_time"]

async def test_patch_trip_not_found(client: AsyncClient):
    trip = copy.deepcopy(DEFAULT_TRIP)
    trip["id"] = 2346332
    trip["driver_id"] = 123

    response = await client.patch(f"/api/trips", json = trip)
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_patch_trip_unprocessable_entity(client: AsyncClient):
    response = await client.patch(f"/api/trips", json = DEFAULT_TRIP)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_delete_trip(client: AsyncClient):    
    driver_id = await create_driver(client, DEFAULT_DRIVER)
    trip = copy.deepcopy(DEFAULT_TRIP)
    trip["driver_id"] = driver_id
    trip_id = await create_trip(client, trip)

    response = await client.delete(f"/api/trips/{trip_id}")
    assert response.status_code == status.HTTP_200_OK

async def test_delete_trip_not_found(client: AsyncClient):
    response = await client.delete(f"/api/trips/1239035234")
    assert response.status_code == status.HTTP_404_NOT_FOUND