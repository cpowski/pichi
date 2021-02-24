from pichi.models.enums import UserStatus, StateAbbreviation, Grant
from pydantic import BaseModel, Field
from typing import List, Dict

CLAIM_USER_MANAGEMENT = "https://chimera.arcadiaanalytics.com/user-management-access/v1"
CLAIM_ENDPOINTS = "https://chimera.arcadiaanalytics.com/endpoints/v1"
CLAIM_CUSTOMER = "https://chimera.arcadiaanalytics.com/customer/v1"
CLAIM_PROFILE = "https://chimera.arcadiaanalytics.com/profile/v1"


class Access(BaseModel):
    """access details"""

    all: bool = Field(alias="all")
    specific: List[str] = Field(alias="specific")


class UserManagementClaim(BaseModel):
    """user management details"""

    apps: Access = Field(alias="apps")
    customers: Access = Field(alias="customers")


class CustomerClaim(BaseModel):
    """customer details"""

    acronym: str = Field(alias="acronym")


class ProfileClaim(BaseModel):
    """profile details"""

    user_id: str = Field(alias="userId")
    user_id_source: str = Field(alias="userIdSource")
    username: str = Field(alias="username")


class Claims(BaseModel):
    """claims model for Auth0"""

    user_id: str = Field(alias="sub")
    scope: str = Field(alias="scope")
    aud: list = Field(alias="aud")
    user_management: UserManagementClaim = Field(alias=CLAIM_USER_MANAGEMENT)
    endpoints: List[str] = Field(alias=CLAIM_ENDPOINTS)
    customer: CustomerClaim = Field(alias=CLAIM_CUSTOMER)
    profile: ProfileClaim = Field(alias=CLAIM_PROFILE)


class UserSummary(BaseModel):
    user_id: str
    given_name: str = Field(default="")
    family_name: str = Field(default="")
    email: str


class UsersSummary(BaseModel):
    users: List[UserSummary]
    total: int


class UserAppMetadata(BaseModel):
    status: UserStatus = Field(default=UserStatus.DEACTIVATED)
    npi: str = Field(default="")
    credentials: str = Field(default="")
    street_address: str = Field(default="", alias="streetAddress")
    city: str = Field(default="")
    state: StateAbbreviation = Field(default=StateAbbreviation.NONE)
    zip: str = Field(default="")
    phone_number: str = Field(default="", alias="phoneNumber")
    migrated: bool = Field(default=False)
    apps: Dict[str, Grant] = Field(default={})


class UserProfile(BaseModel):
    email: str
    given_name: str
    family_name: str
    app_metadata: UserAppMetadata
