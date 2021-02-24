from pydantic import BaseModel


class AppAccessSetting(BaseModel):
    application: str
    granularity: str
    name: str
    callback_url: str
    allow_access_by_default: bool
