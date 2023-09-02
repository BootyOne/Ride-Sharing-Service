from src.auth.models import User
from src.auth.utils import get_current_user
from src.regions.models import Country, City
from src.regions.utils import get_all_regions_from_db
from src.regions.schemas import RegionCreate, RegionsRead

from typing import List

from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(
    prefix='/Regions',
    tags=['Regions']
)


@router.post("/add")
async def add_region(region: RegionCreate, user: User = Depends(get_current_user)):
    if region.country:
        country, created = Country.get_or_create(name=region.country)
        if region.city:
            City.create(name=region.city, country_id=country.id, latitude=region.city_latitude, longitude=region.city_longitude)
    return {"status": "Region added"}


@router.get("/get_all", response_model=List[RegionsRead])
async def read_regions(user: User = Depends(get_current_user)):
    regions = get_all_regions_from_db()
    if not regions:
        raise HTTPException(status_code=404, detail="Regions not found")
    return regions
