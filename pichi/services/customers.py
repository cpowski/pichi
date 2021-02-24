from pichi.models.api import Customer
from pichi.services.dynamo import scan, get_table
from typing import List


def map_customer_item(item) -> Customer:
    """map a single item from customers table to a customer"""
    return Customer(
        customer_acronym=item["customerAcronym"], core_web_url=item["coreWebURL"]
    )


def map_customer_items(items) -> List[Customer]:
    """map items from customers table to list of customers"""
    return list(map(map_customer_item, items))


def get_all_customers() -> List[Customer]:
    """return all items in customers table"""
    scan_kwargs = {
        "ProjectionExpression": "customerAcronym, coreWebURL",
    }

    return scan("chimera-local-Customers", map_customer_items, **scan_kwargs)


def get_specific_customers(customer_keys: List[str]) -> List[Customer]:
    """return matching customers from the customers table"""
    table = get_table("chimera-local-Customers")
    customers = list()
    for key in customer_keys:
        response = table.get_item(Key={"customerAcronym": key})
        customers.append(map_customer_item(response["Item"]))

    return customers
