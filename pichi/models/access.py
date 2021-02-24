from pydantic import BaseModel
from typing import List


class AllowedApp(BaseModel):
    name: str
    identifier: str
    order: int


class UserAccess(BaseModel):
    allowed_apps: List[AllowedApp]
    disallowed_apps: List[AllowedApp]
