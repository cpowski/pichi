from boto3.dynamodb.conditions import Key
from pichi.models.settings import AppAccessSetting
from pichi.services.dynamo import scan
from typing import List


def map_app_access_setting_item(item) -> AppAccessSetting:
    return AppAccessSetting(
        application=item["application"],
        granularity=item["granularity"],
        name=item["name"],
        callback_url=item["callbackUrl"],
        allow_access_by_default=item["allowAccessByDefault"],
    )


def map_app_access_setting_items(items) -> List[AppAccessSetting]:
    return list(map(map_app_access_setting_item, items))


def all_app_access_settings(customer_acronym: str) -> List[AppAccessSetting]:
    scan_kwargs = {
        "FilterExpression": Key("granularity").eq(
            f"app-level-access-{customer_acronym}"
        ),
    }
    return scan("chimera-local-Setting", map_app_access_setting_items, **scan_kwargs)
