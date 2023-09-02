from pydantic import BaseModel
from datetime import datetime


class TripCreate(BaseModel):
    driver_id: int
    description: str
    start_time: datetime
    end_time: datetime
    departure_country_id: int
    departure_city_id: int
    arrival_country_id: int
    arrival_city_id: int


class TripStatusCreate(BaseModel):
    name: str


class TripStatusUpdate(BaseModel):
    status: str
