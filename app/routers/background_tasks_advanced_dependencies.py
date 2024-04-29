from fastapi import APIRouter, status, Response, Path, Depends, BackgroundTasks
from typing import Union, List, Annotated
from app.schemas.default_response import DefaultResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
import time

router = APIRouter(
    prefix="/api/background_tasks_advanced_dependencies", 
    tags=["backgroundTasksAdvancedDependencies"]
)

def print_timestamp():
    time.sleep(2)
    print(time.time())

@router.get("/get_time", status_code=status.HTTP_200_OK)
async def read_drivers(background_tasks: BackgroundTasks):
    background_tasks.add_task(print_timestamp)
    return JSONResponse(content={"current_time": time.time()})

class NameChecker:
    def __init__(self):
        pass
    
    def __call__(self, name: str = ""):        
        return name and len(name) > 0
    
checker = NameChecker()

@router.get("/check", status_code=status.HTTP_200_OK)
async def read_drivers(name_checker: Annotated[bool, Depends(checker)], name: str = ""):
    return JSONResponse(content={"result": name if name_checker else "Параметр отсутствует"})
