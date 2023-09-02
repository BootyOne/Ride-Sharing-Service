from fastapi import APIRouter, HTTPException, Depends

from src.auth.utils import get_current_user
from src.auth.models import User
from src.drive.models import TripsStatuses, Trips, UserTrips
from src.drive.schemas import TripStatusCreate, TripCreate, TripStatusUpdate

# from src.drive.utils import book_drive, confirm_drive

router = APIRouter(
    prefix='/Drives',
    tags=['Drives']
)


@router.post("/trips/statuses/")
async def add_trip_status(status: TripStatusCreate):
    TripsStatuses.create(name=status.name)
    return {"status": "Trip status added"}


@router.post("/trips/")
async def create_trip(trip: TripCreate):
    driver = User.get(User.id == trip.driver_id)
    required_fields = [driver.car_make, driver.car_number, driver.phone_number,
                       driver.first_name, driver.second_name, driver.about_me, driver.is_male]
    if not all(required_fields):
        raise HTTPException(status_code=400, detail="Driver profile incomplete")

    Trips.create(**trip.dict())
    return {"status": "Trip created"}


@router.delete("/trips/{trip_id}/")
async def delete_trip(trip_id: int):
    query = Trips.delete().where(Trips.id == trip_id)
    deleted_rows = query.execute()

    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Trip not found")

    return {"status": "Trip deleted"}


@router.patch("/trips/{trip_id}/status/")
async def update_trip_status(trip_id: int, status: TripStatusUpdate):
    query = Trips.update(status=status.status).where(Trips.id == trip_id)
    updated_rows = query.execute()

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Trip not found")

    return {"status": "Trip status updated"}


@router.post("/trips/register/")
async def register_for_trip(trip_id: int, user: User = Depends(get_current_user)):
    trip = Trips.get_by_id(trip_id)
    if trip.reserved_seats >= trip.total_seats:
        return {"error": "No seats available"}
    UserTrips.create(trip_id=trip_id, user_id=user.id)
    return {"status": "Registered for trip"}


@router.delete("/trips/unregister/")
async def unregister_for_trip(trip_id: int, user: User = Depends(get_current_user)):
    query = UserTrips.delete().where((UserTrips.trip == trip_id) & (UserTrips.id == user.id))
    deleted_rows = query.execute()

    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Registration not found")

    return {"status": "Unregistered for trip"}
