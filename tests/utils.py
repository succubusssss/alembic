from httpx import AsyncClient

async def create_user(client: AsyncClient, user):
    response = await client.post("/api/users", json = user)
    user_id = response.json()["user_id"]
    return user_id

async def create_driver(client: AsyncClient, user):
    response = await client.post("/api/drivers", json = user)
    driver_id = response.json()["driver_id"]
    return driver_id

async def create_trip(client: AsyncClient, user):
    response = await client.post("/api/trips", json = user)
    trips_id = response.json()["trip_id"]
    return trips_id