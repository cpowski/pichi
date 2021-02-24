from fastapi import APIRouter, Depends
from pichi.api.dependencies.auth0 import get_current_user
from pichi.models.api import Customer
from pichi.services.customers import get_all_customers
from typing import List

router = APIRouter()


@router.get(
    "",
    response_model=List[Customer],
    name="customers:get-customers",
    dependencies=[Depends(get_current_user)],
)
async def get_customers():
    return get_all_customers()
