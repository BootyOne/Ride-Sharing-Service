from src.auth.schemas import UserUpdate
from src.regions.schemas import RegionsRead, CityRead

from datetime import datetime
from typing import List

from pydantic import BaseModel


class TripCreate(BaseModel):
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
    status: int


class TripsStatusRead(BaseModel):
    id: int
    status: str


class TripRead(BaseModel):
    id: int
    driver: UserUpdate
    description: str
    start_time: str
    end_time: str
    departure_country: RegionsRead
    departure_city: CityRead
    arrival_country: RegionsRead
    arrival_city: CityRead
    status: TripsStatusRead
    total_seats: int
    reserved_seats: int


class TripsRead(BaseModel):
    trips: List[TripRead]


class UserTripRead(BaseModel):
    id: int
    trip: TripRead


class UserTripsRead(BaseModel):
    trips: List[UserTripRead]
