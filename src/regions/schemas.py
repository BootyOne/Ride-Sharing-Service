from typing import List

from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    latitude: float
    longitude: float


class RegionCreate(BaseModel):
    country: str
    city: CityCreate


class CityRead(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

class RegionsRead(BaseModel):
    id: int
    name: str
    cities: List[CityRead]