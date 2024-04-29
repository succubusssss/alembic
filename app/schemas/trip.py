from pydantic import Field
from datetime import datetime
from typing import Union, Annotated
from app.schemas.base import BaseSchema

class Trip(BaseSchema):
    driver_id: Annotated[int, Field(gt=0)]
    departure_time: datetime

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "1",
                "driver_id": "2",
                "departure_time": "2024-01-06 22:01:02"
            }
        }

class CreateTrip(Trip):
    id: None = None

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "driver_id": "2",
                "departure_time": "2024-01-06 22:01:02"
            }
        }

class UpdateTrip(Trip):
    pass

class PatchTrip(Trip):
    driver_id: Annotated[Union[int, None], Field(gt=0)] = None
    departure_time: Union[datetime, None] = None