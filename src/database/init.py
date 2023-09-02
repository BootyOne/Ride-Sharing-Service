from src.auth.models import User
from src.regions.models import Country, City
from src.drive.models import Trips, TripsStatuses, UserTrips
from src.database.database import database_proxy

from peewee_migrate import Router

router = Router(database_proxy)
router.create(auto=[User, City, Country, Trips, TripsStatuses, UserTrips])
router.run()
