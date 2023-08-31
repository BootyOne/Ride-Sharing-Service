from src.auth.models import User, Role
from src.database.database import database_proxy

from peewee_migrate import Router

router = Router(database_proxy)
# router.create(auto=[User, Role])
router.run()
