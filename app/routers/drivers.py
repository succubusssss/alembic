from fastapi import APIRouter, status, Response, Path, Depends
from typing import Union, List
from app.schemas.default_response import DefaultResponse
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.models.driver import Driver
from app.schemas.driver import Driver as DriverSchema, CreateDriver, UpdateDriver, PatchDriver
from app.repository import crud

router = APIRouter(
    prefix="/api", 
    tags=["driver"]
)

responses = {
    status.HTTP_404_NOT_FOUND: {"model": DefaultResponse, "description": "Item not found"}
}

@router.get("/drivers", response_model=Union[List[DriverSchema], None], status_code=status.HTTP_200_OK)
async def read_drivers(db: AsyncSession = Depends(get_db)):
    all_drivers = await crud.get_all(Driver, db)
    return all_drivers

@router.get("/drivers/{id}", response_model=Union[DriverSchema, DefaultResponse], responses={**responses, status.HTTP_200_OK: {"model": DriverSchema}})
async def get_driver(id: int, response: Response, db: AsyncSession = Depends(get_db)):
    driver: Driver = await crud.get_by_id(Driver, id, db)
    if driver == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Driver not found")
    
    return driver

@router.post("/drivers", status_code=status.HTTP_200_OK)
async def create_driver(driver: CreateDriver, db: AsyncSession = Depends(get_db)):
    driver: Driver = await crud.create(Driver, driver, db)
    return JSONResponse(content={"driver_id": driver.id})

@router.put("/drivers", response_model=Union[UpdateDriver, DefaultResponse], responses={**responses, status.HTTP_200_OK: {"model": DriverSchema}})
async def update_driver(driver: DriverSchema, response: Response, db: AsyncSession = Depends(get_db)):
    updated_driver: DriverSchema = await crud.update(Driver, driver, db)
    if updated_driver == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Driver not found")

    return updated_driver

@router.patch("/drivers", response_model=Union[PatchDriver, DefaultResponse], responses={**responses, status.HTTP_200_OK: {"model": DriverSchema}})
async def patch_driver(driver: PatchDriver, response: Response, db: AsyncSession = Depends(get_db)):
    updated_driver: DriverSchema = await crud.update(Driver, driver, db)
    if updated_driver == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Driver not found")

    return updated_driver

@router.delete("/drivers/{id}", response_model=DefaultResponse, responses={**responses, status.HTTP_200_OK: {"model": DefaultResponse}})
async def remove_driver(id: int, response: Response, db: AsyncSession = Depends(get_db)):
    driver: Driver = await crud.get_by_id(Driver, id, db)
    if driver == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="Driver not found")
    
    await crud.delete(Driver, id, db)

    return DefaultResponse(success=True, message="Driver successfully removed") 