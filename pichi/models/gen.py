# generated by fastapi-codegen:
#   filename:  tmp/apps/api/openapi.json
#   timestamp: 2021-02-18T16:04:23+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, Field


class DataDto(BaseModel):
    message: str


class BoolSettingSpecifics(BaseModel):
    default: bool


class BoolSettingDto(BaseModel):
    name: str
    description: str
    identifier: str
    scope: str
    customerAcronym: str
    setting: BoolSettingSpecifics


class SelectOneSettingSpecifics(BaseModel):
    default: str
    options: List[str]


class SelectOneSettingDto(BaseModel):
    name: str
    description: str
    identifier: str
    scope: str
    customerAcronym: str
    setting: SelectOneSettingSpecifics


class SelectManySettingDto(BaseModel):
    name: str
    description: str
    identifier: str
    scope: str
    customerAcronym: str


class SettingSpecificsUpdateDto(BaseModel):
    default: Dict[str, Any]
    options: List[str]


class SettingUpdateDto(BaseModel):
    name: str
    description: str
    setting: SettingSpecificsUpdateDto


class AllowedAppDto(BaseModel):
    name: str
    identifier: str
    order: float


class UserAccessDto(BaseModel):
    allowedApps: List[AllowedAppDto]
    disallowedApps: List[AllowedAppDto]


class UserGrantsDto(BaseModel):
    providers: List[str]
    plans: List[str]
    legacyPlans: Optional[List[str]] = None
    sources: List[str]
    userType: Dict[str, Any]
    userId: str
    customerAcronym: str


class GlobalUserGrants(BaseModel):
    providers: List[str]
    plans: List[str]
    legacyPlans: Optional[List[str]] = None
    sources: List[str]
    userType: Dict[str, Any]
    allProviders: bool
    allSources: bool
    allPlans: bool


class GlobalSettingNodeDto(BaseModel):
    id: str
    legacy_id: float
    name: str
    path: List[str]
    children: List[GlobalSettingNodeDto]
    disabled: bool


class GlobalSettingsDto(BaseModel):
    providers: List[GlobalSettingNodeDto]
    plans: List[GlobalSettingNodeDto]
    sources: List[GlobalSettingNodeDto]


class UserProfileV1(BaseModel):
    email: str
    firstName: str
    lastName: str
    phoneNumber: str
    npi: str
    credentials: str
    streetAddress: str
    city: str
    state: str
    zip: str


class App(BaseModel):
    class Config:
        extra = Extra.allow

    __root__: Any


class CompleteUserGrantsDto(BaseModel):
    global_: GlobalUserGrants = Field(..., alias="global")
    app: Dict[str, App]
    profile: UserProfileV1


class UserGrantsUpdateDto(BaseModel):
    providers: List[str]
    plans: List[str]
    legacyPlans: Optional[List[str]] = None
    sources: List[str]
    userType: Dict[str, Any]
    customerAcronym: str


class SettingsByAppDto(BaseModel):
    pass


class CreateUserDto(BaseModel):
    email: str
    username: Optional[str] = None
    password: str
    firstName: str
    lastName: str
    npi: str
    credentials: str
    streetAddress: str
    city: str
    state: str
    zip: str
    phoneNumber: str
    global_: UserGrantsUpdateDto = Field(..., alias="global")


class UserDto(BaseModel):
    email: str
    username: Optional[str] = None
    password: str
    firstName: str
    lastName: str
    npi: str
    credentials: str
    streetAddress: str
    city: str
    state: str
    zip: str
    phoneNumber: str
    global_: UserGrantsUpdateDto = Field(..., alias="global")
    userId: str


class State(Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"


class UserProfileDto(BaseModel):
    status: str
    email: str
    firstName: str
    lastName: str
    npi: str
    credentials: str
    streetAddress: str
    city: str
    state: State
    zip: str
    phoneNumber: str


class State1(Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"


class UpdateUserProfileDto(BaseModel):
    status: str
    email: str
    firstName: str
    lastName: str
    npi: str
    credentials: str
    streetAddress: str
    city: str
    state: State1
    zip: str
    phoneNumber: str


class UserSummaryDto(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str


class UsersSummaryDto(BaseModel):
    users: UserSummaryDto
    total: float


class UsersSearchResultsDtoV1(BaseModel):
    pass


class CreateUserWithoutGrantsDto(BaseModel):
    email: str
    username: Optional[str] = None
    password: str
    firstName: str
    lastName: str
    npi: str
    credentials: str
    streetAddress: str
    city: str
    state: str
    zip: str
    phoneNumber: str


class UpdatePasswordDto(BaseModel):
    newPassword: str


class AppMetaDataDto(BaseModel):
    streetAddress: str
    credentials: str
    city: str
    state: str
    zip: str
    phoneNumber: str
    npi: str


class Auth0UserDto(BaseModel):
    id: str
    email: str
    email_verified: bool
    app_metadata: AppMetaDataDto


class Auth0Connection(BaseModel):
    name: str


class Auth0Context(BaseModel):
    connection: Auth0Connection


class UserPostRegistrationDto(BaseModel):
    auth0User: Auth0UserDto
    auth0Context: Auth0Context
    actionPerformedByUserId: str


class CognitoUserValidityReqDto(BaseModel):
    userPoolId: str
    appClientId: str
    userName: str
    password: str


class CognitoUserValidityDto(BaseModel):
    userPoolId: str
    appClientId: str
    userName: str
    valid: bool
