from fastapi import APIRouter
from pichi.api.routes import app, customers, users

router = APIRouter()

router.include_router(app.router, tags=["app"])
router.include_router(customers.router, prefix="/customers", tags=["customers"])
router.include_router(users.router, prefix="/users", tags=["users"])
