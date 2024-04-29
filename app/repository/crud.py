from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import BaseModel
from app.schemas.base import BaseSchema
from sqlalchemy.future import select

# base CRUD operations
async def get_by_id(model: BaseModel, id: int, db: AsyncSession):
    return await db.get(model, id)

async def get_all(model: BaseModel, db: AsyncSession):
    result = await db.execute(select(model))
    return result.scalars().all()

async def create(model: BaseModel, schema: BaseSchema, db: AsyncSession):
    db_model = model(**schema.model_dump())
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return db_model

async def update(model: BaseModel, schema: BaseSchema, db: AsyncSession):
    db_model = await get_by_id(model, schema.id, db)
    if db_model is None:
        return None
    
    for var, value in vars(schema).items():
        setattr(db_model, var, value) if value else None

    await db.commit()
    await db.refresh(db_model)
    return db_model

async def delete(model: BaseModel, id: int, db: AsyncSession):
    db_user = await get_by_id(model, id, db)
    if db_user is None:
        return
    
    await db.delete(db_user)
    await db.commit()