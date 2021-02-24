from fastapi_camelcase import CamelModel
from pichi.models.enums import UserStatus, StateAbbreviation, UserType
from pydantic import Field
from typing import List


class Message(CamelModel):
    message: str


class Customer(CamelModel):
    customer_acronym: str
    core_web_url: str


class UserSummary(CamelModel):
    id: str
    first_name: str
    last_name: str
    email: str


class UsersSummary(CamelModel):
    users: List[UserSummary]
    total: int


class AppMetadata(CamelModel):
    npi: str
    credentials: str
    street_address: str
    city: str
    state: StateAbbreviation
    zip: str
    phone_number: str


class UserProfile(AppMetadata):
    status: UserStatus
    email: str
    first_name: str
    last_name: str


class User(CamelModel):
    id: str
    email: str
    email_verified: bool
    app_metadata: AppMetadata


class UserGrants(CamelModel):
    customer_acronym: str
    providers: List[str]
    plans: List[str]
    legacy_plans: List[str] = Field(default=list())
    sources: List[str]
    user_type: UserType


class CreateUser(CamelModel):
    email: str
    username: str = Field(default="")
    password: str
    first_name: str
    last_name: str
    npi: str = Field(default="")
    credentials: str = Field(default="")
    street_address: str = Field(default="")
    city: str = Field(default="")
    state: StateAbbreviation = Field(default=StateAbbreviation.NONE)
    zip: str = Field(default="")
    phone_number: str = Field(default="")
    global_grants: UserGrants = Field(alias="global")
