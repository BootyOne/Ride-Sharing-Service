from datetime import datetime

from fastapi import APIRouter, HTTPException

from src.regions.models import Country, City
from src.regions.schemas import RegionCreate
from src.auth.models import User, Role
from src.auth.utils import verify_password, get_password_hash, create_access_token
from peewee import DoesNotExist
from pydantic import BaseModel
from fastapi import Response, Request
from fastapi.security import HTTPBearer

router = APIRouter(
    prefix='/Regions',
    tags=['Regions']
)


@router.post("/regions/")
async def add_region(region: RegionCreate):
    if region.country:
        country, created = Country.get_or_create(name=region.country)
        if region.city:
            City.create(name=region.city, country_id=country.id, latitude=region.city_latitude, longitude=region.city_longitude)
    return {"status": "Region added"}
