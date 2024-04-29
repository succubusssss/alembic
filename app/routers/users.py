from fastapi import APIRouter, status, Response, Path, Depends
from typing import Union, List
from app.schemas.default_response import DefaultResponse
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.models.user import User
from app.schemas.user import User as UserSchema, CreateUser, UpdateUser, PatchUser
from app.repository import crud

router = APIRouter(
    prefix="/api", 
    tags=["user"]
)

responses = {
    status.HTTP_404_NOT_FOUND: {"model": DefaultResponse, "description": "Item not found"}
}

@router.get("/users", response_model=Union[List[UserSchema], None], status_code=status.HTTP_200_OK)
async def read_users(db: AsyncSession = Depends(get_db)):
    all_users = await crud.get_all(User, db)
    return all_users

@router.get("/users/{id}", response_model=Union[UserSchema, DefaultResponse], responses={**responses, status.HTTP_200_OK: {"model": UserSchema}})
async def get_user(id: int, response: Response, db: AsyncSession = Depends(get_db)):
    user: User = await crud.get_by_id(User, id, db)
    if user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="User not found")
    
    return user   

@router.post("/users", status_code=status.HTTP_200_OK)
async def create_user(user: CreateUser, db: AsyncSession = Depends(get_db)):
    user: User = await crud.create(User, user, db)
    return JSONResponse(content={"user_id": user.id})

@router.put("/users", response_model=Union[UpdateUser, DefaultResponse], responses={**responses, status.HTTP_200_OK: {"model": UserSchema}})
async def update_user(user: UpdateUser, response: Response, db: AsyncSession = Depends(get_db)):
    updated_user: UserSchema = await crud.update(User, user, db)
    if updated_user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="User not found")

    return updated_user

@router.patch("/users", response_model=Union[PatchUser, DefaultResponse], responses={**responses, status.HTTP_200_OK: {"model": UserSchema}})
async def patch_user(user: PatchUser, response: Response, db: AsyncSession = Depends(get_db)):
    updated_user: UserSchema = await crud.update(User, user, db)
    if updated_user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="User not found")

    return updated_user

@router.delete("/users/{id}", response_model=DefaultResponse, responses={**responses, status.HTTP_200_OK: {"model": DefaultResponse}})
async def remove_user(id: int, response: Response, db: AsyncSession = Depends(get_db)):
    user: User = await crud.get_by_id(User, id, db)
    print(user)
    if user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="User not found")
    
    await crud.delete(User, id, db)

    return DefaultResponse(success=True, message="User successfully removed") 