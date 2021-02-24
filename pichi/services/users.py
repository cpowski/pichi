from pichi.models.api import (
    UsersSummary,
    UserSummary,
    UserProfile,
    User,
    AppMetadata,
    CreateUser,
)
from pichi.models.auth0 import (
    UsersSummary as Auth0UsersSummary,
    UserSummary as Auth0UserSummary,
    UserProfile as Auth0UserProfile,
)
from pichi.models.enums import StateAbbreviation
from pichi.services.auth0 import Auth0Service


def map_user_summary(user: Auth0UserSummary) -> UserSummary:
    return UserSummary(
        id=user.user_id,
        first_name=user.given_name,
        last_name=user.family_name,
        email=user.email,
    )


def map_users_summary(summary: Auth0UsersSummary) -> UsersSummary:
    return UsersSummary(
        total=summary.total,
        users=list(map(map_user_summary, summary.users)),
    )


def map_user_profile(profile: Auth0UserProfile) -> UserProfile:
    return UserProfile(
        email=profile.email,
        first_name=profile.given_name,
        last_name=profile.family_name,
        status=profile.app_metadata.status,
        npi=profile.app_metadata.npi,
        credentials=profile.app_metadata.credentials,
        street_address=profile.app_metadata.street_address,
        city=profile.app_metadata.city,
        state=profile.app_metadata.state,
        zip=profile.app_metadata.zip,
        phone_number=profile.app_metadata.phone_number,
    )


def users_page(
    auth0: Auth0Service,
    customer_acronym: str,
    page: int,
    per_page: int,
    search: str,
) -> UsersSummary:
    result = auth0.users(customer_acronym, page, per_page, search)
    return map_users_summary(result)


def user_profile(
    auth0: Auth0Service, user_id: str, customer_acronym: str
) -> UserProfile:
    result = auth0.user_profile(user_id, customer_acronym)
    return map_user_profile(result)


def create(
    auth0: Auth0Service,
    dto: CreateUser,
    current_user_id: str,
    customer_acronym: str,
) -> User:
    # validate

    auth0.register_user()
    return User(
        id="",
        email="",
        email_verified=False,
        app_metadata=AppMetadata(
            npi="",
            credentials="",
            street_address="",
            city="",
            state=StateAbbreviation.NONE,
            zip="",
            phone_number="",
        ),
    )
