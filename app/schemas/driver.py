from pydantic import Field
from datetime import date
from typing import Union, Annotated
from app.schemas.base import BaseSchema
from app.schemas.trip import Trip

class Driver(BaseSchema):
    last_name: Annotated[str, Field(min_length=2, max_length=30)]
    first_name: Annotated[str, Field(min_length=2, max_length=30)]
    patronymic: Annotated[str, Field(min_length=2, max_length=30)]
    passport: Annotated[str, Field(max_length=10, min_length=10, pattern=r'^\d*$')]
    experience: date
    
    trips: list[Trip] = []

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "1",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "patronymic": "Отчество",
                "passport": "0123456789",
                "experience": "2024-01-06"
            }
        }

class CreateDriver(Driver):
    id: None = None

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "last_name": "Фамилия",
                "first_name": "Имя",
                "patronymic": "Отчество",
                "passport": "0123456789",
                "experience": "2024-01-06"
            }
        }

class UpdateDriver(Driver):
    pass

class PatchDriver(Driver):
    last_name: Annotated[Union[str, None], Field(min_length=2, max_length=30)] = None
    first_name: Annotated[Union[str, None], Field(min_length=2, max_length=30)] = None
    patronymic: Annotated[Union[str, None], Field(min_length=2, max_length=30)] = None
    passport: Annotated[Union[str, None], Field(max_length=10, min_length=10, pattern=r'^\d*$')] = None
    experience: Union[date, None] = None