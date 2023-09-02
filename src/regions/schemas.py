from pydantic import BaseModel

from typing import List


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


class CityRemove(BaseModel):
    name: str


class RegionRemove(BaseModel):
    country: str
    city: CityRemove
