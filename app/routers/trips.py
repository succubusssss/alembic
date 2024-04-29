from fastapi import APIRouter, status, Response, Path, Depends
from typing import Union, List
from app.schemas.default_response import DefaultResponse
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.models.trip import Trip
from app.models.driver import Driver
from app.schemas.trip import Trip as TripSchema, CreateTrip, UpdateTrip, PatchTrip
from app.repository import crud

router = APIRouter(
    prefix="/api", 
    tags=["trip"]
)

responses = {
    status.HTTP_404_NOT_FOUND: {"model": DefaultResponse, "description": "Item not found"}
}

@router.get("/trips", response_model=Union[List[TripSchema], None], status_code=status.HTTP_200_OK)
async def read_trips(db: AsyncSession = Depends(get_db)):
    all_trips = await crud.get_all(Trip, db)
    return all_trips

@router.get("/trips/{id}", response_model=Union[TripSchema, DefaultResponse], responses={**responses, status.HTTP_200_OK: {"model": TripSchema}})
async def get_trip(id: int, response: Response, db: AsyncSession = Depends(get_db)):
    trip: Trip = await crud.get_by_id(Trip, id, db)
    if trip == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Trip not found")
    
    return trip

@router.post(
        "/trips", 
        responses={status.HTTP_404_NOT_FOUND: {"description": "Trip with such id not found"}, status.HTTP_200_OK: {"description": "Trip successfully created"}}
)
async def create_trip(trip: CreateTrip, response: Response, db: AsyncSession = Depends(get_db)):
    driver: Driver = await crud.get_by_id(Driver, trip.driver_id, db)
    if driver is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Trip with such id not found")
    
    trip: Trip = await crud.create(Trip, trip, db)
    return JSONResponse(content={"trip_id": trip.id})

@router.put("/trips", response_model=Union[UpdateTrip, DefaultResponse], responses={**responses, status.HTTP_200_OK: {"model": TripSchema}})
async def update_trip(trip: TripSchema, response: Response, db: AsyncSession = Depends(get_db)):
    driver: Driver = await crud.get_by_id(Driver, trip.driver_id, db)
    if driver is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Trip with such id not found")
    
    updated_trip: TripSchema = await crud.update(Trip, trip, db)
    if updated_trip == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Trip not found")

    return updated_trip

@router.patch("/trips", response_model=Union[PatchTrip, DefaultResponse], responses={**responses, status.HTTP_200_OK: {"model": TripSchema}})
async def patch_trip(trip: PatchTrip, response: Response, db: AsyncSession = Depends(get_db)):
    if trip.driver_id is not None:
        driver: Driver = await crud.get_by_id(Driver, trip.driver_id, db)
        if driver is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return DefaultResponse(success=False, message="Trip with such id not found")

    updated_trip: TripSchema = await crud.update(Trip, trip, db)
    if updated_trip == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Trip not found")

    return updated_trip

@router.delete("/trips/{id}", response_model=DefaultResponse, responses={**responses, status.HTTP_200_OK: {"model": DefaultResponse}})
async def remove_trip(id: int, response: Response, db: AsyncSession = Depends(get_db)):
    trip: Trip = await crud.get_by_id(Trip, id, db)
    if trip == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Trip not found")
    
    await crud.delete(Trip, id, db)

    return DefaultResponse(success=True, message="Trip successfully removed") 