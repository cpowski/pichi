from pichi.core.config import DYNAMODB_ENDPOINT
import boto3


def get_table(table_name):
    dynamodb = boto3.resource("dynamodb", endpoint_url=DYNAMODB_ENDPOINT)
    # aws_access_key_id="anything",
    # aws_secret_access_key="anything",
    # region_name="us-east-1")

    return dynamodb.Table(table_name)


def scan(table_name: str, mapper, **kwargs):
    table = get_table(table_name)
    result = list()
    done = False
    start_key = None
    while not done:
        if start_key:
            kwargs["ExclusiveStartKey"] = start_key
        response = table.scan(**kwargs)
        result.extend(mapper(response.get("Items", [])))
        start_key = response.get("LastEvaluatedKey", None)
        done = start_key is None

    return result
