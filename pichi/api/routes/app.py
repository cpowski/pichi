from fastapi import APIRouter
from pichi.models.api import Message
import pichi.services.app as app_services

router = APIRouter()


@router.get("/heartbeat", response_model=Message, name="app:get-heartbeat")
async def get_heartbeat():
    return app_services.get_heartbeat()
