from pydantic import Field
from typing import Union, Annotated
from app.schemas.base import BaseSchema

class User(BaseSchema):
    last_name: Annotated[str, Field(min_length=2, max_length=30)]
    first_name: Annotated[str, Field(min_length=2, max_length=30)]
    patronymic: Annotated[str, Field(min_length=2, max_length=30)]
    group: Annotated[str, Field(min_length=2, max_length=10)]

    class ConfigDict:
        from_attributes=True
        json_schema_extra = {
            "example": {
                "id": "1",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "patronymic": "Отчество",
                "group": "Группа"
            }
        }

class CreateUser(User):
    id: None = None
    
    class ConfigDict:
        from_attributes=True
        json_schema_extra = {
            "example": {
                "last_name": "Фамилия",
                "first_name": "Имя",
                "patronymic": "Отчество",
                "group": "Группа"
            }
        }

class UpdateUser(User):
    pass

class PatchUser(User):
    last_name: Annotated[Union[str, None], Field(min_length=2, max_length=30)] = None
    first_name: Annotated[Union[str, None], Field(min_length=2, max_length=30)] = None
    patronymic: Annotated[Union[str, None], Field(min_length=2, max_length=30)] = None
    group: Annotated[Union[str, None], Field(min_length=2, max_length=10)] = None