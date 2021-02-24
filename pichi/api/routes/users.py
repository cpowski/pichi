from fastapi import APIRouter, Depends, Query, HTTPException, status
from pichi.api.dependencies.auth0 import get_current_user, get_auth0_service
from pichi.models.api import UsersSummary, UserProfile, User, CreateUser
from pichi.models.auth0 import Claims
from pichi.services.access import user_has_access_to_user_management
from pichi.services.auth0 import Auth0Service
from pichi.services.users import users_page, user_profile, create
from typing import Optional

router = APIRouter()


@router.get("", response_model=UsersSummary, name="users:get-users")
async def get_users(
    user: Claims = Depends(get_current_user),
    auth0: Auth0Service = Depends(get_auth0_service),
    customer_acronym: str = Query("", alias="customerAcronym"),
    page: int = Query(0, alias="page"),
    per_page: int = Query(50, alias="perPage"),
    search: Optional[str] = Query(None, alias="search"),
):
    if not user_has_access_to_user_management(auth0, user.user_id, customer_acronym):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You do not have access to User Management"
        )

    return users_page(auth0, customer_acronym, page, per_page, search)


@router.get("/{user_id}/profile", response_model=UserProfile, name="users:get-profile")
async def get_profile(
    user_id: str,
    customer_acronym: str = Query("", alias="customerAcronym"),
    user: Claims = Depends(get_current_user),
    auth0: Auth0Service = Depends(get_auth0_service),
):
    if not user_has_access_to_user_management(auth0, user.user_id, customer_acronym):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You do not have access to User Management"
        )

    return user_profile(auth0, f"auth0|{user_id}", customer_acronym)


@router.post("", response_model=User, name="users:create-user")
async def create_user(
    dto: CreateUser,
    customer_acronym: str = Query("", alias="customerAcronym"),
    user: Claims = Depends(get_current_user),
    auth0: Auth0Service = Depends(get_auth0_service),
):
    if not user_has_access_to_user_management(auth0, user.user_id, customer_acronym):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You do not have access to User Management"
        )

    return create(auth0, dto, user.user_id, customer_acronym)
