from pichi.models.access import UserAccess, AllowedApp
from pichi.models.auth0 import Grant
from pichi.models.settings import AppAccessSetting
from pichi.services.app_access_settings import all_app_access_settings
from pichi.services.auth0 import Auth0Service
from typing import Dict

USER_MANAGEMENT_ID = "user-management"


def app_accessible(app: AppAccessSetting, user_apps: Dict[str, Grant]) -> bool:
    if app.application not in user_apps:
        return False

    return user_apps[app.application] == Grant.ALLOW or (
        app.allow_access_by_default and user_apps[app.application] != Grant.DENY
    )


def map_user_access(setting: AppAccessSetting, index: int) -> AllowedApp:
    return AllowedApp(
        name=setting.name,
        identifier=setting.application,
        order=index,
    )


def get_access(auth0: Auth0Service, user_id: str, customer_acronym: str) -> UserAccess:
    metadata = auth0.user_app_metadata(user_id)
    settings = all_app_access_settings(customer_acronym)

    return UserAccess(
        allowed_apps=[
            map_user_access(setting, settings.index(setting))
            for setting in settings
            if app_accessible(setting, metadata.apps)
        ],
        disallowed_apps=[
            map_user_access(setting, settings.index(setting))
            for setting in settings
            if not app_accessible(setting, metadata)
        ],
    )


def user_has_access_to_user_management(
    auth0: Auth0Service, user_id: str, customer_acronym: str
) -> bool:
    access = get_access(auth0, user_id, customer_acronym)
    for app in access.allowed_apps:
        if app.identifier == USER_MANAGEMENT_ID:
            return True

    return False
