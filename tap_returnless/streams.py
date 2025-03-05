"""Stream type classes for tap-returnless."""

from __future__ import annotations

import typing as t
from importlib import resources
from urllib.parse import parse_qsl, urlparse, ParseResult

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_returnless.client import ReturnlessStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class Attachments(ReturnlessStream):
    """Attachments stream class."""

    name = "attachments"
    path = "/attachments"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "attachments.json"


class Categories(ReturnlessStream):
    """Categories stream class."""

    name = "categories"
    path = "/categories"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "categories.json"


class Countries(ReturnlessStream):
    """Countries stream class."""

    name = "countries"
    path = "/countries"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "countries.json"


class Depreciations(ReturnlessStream):
    """Depreciations stream class."""

    name = "depreciations"
    path = "/depreciations"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "updated_at"
    schema_filepath = SCHEMAS_DIR / "depreciations.json"


class Forms(ReturnlessStream):
    """Forms stream class."""

    name = "forms"
    path = "/forms"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "forms.json"

    def get_child_context(self, record, context):
        """Pass form_id to child streams."""
        return {"form_id": record["id"]}

    def get_url_params(self, context, next_page_token):

        params: dict = {"include": "locale,locales"}

        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params


class FormReturnReasons(ReturnlessStream):
    """FormReturnReasons stream class."""

    name = "form_return_reasons"
    path = "/forms/{form_id}/return-reasons"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "form_return_reasons.json"

    parent_stream_type = Forms
    ignore_parent_replication_key = True

    def get_child_context(self, record, context):
        return super().get_child_context(record, context)


class FormShippingMethods(ReturnlessStream):
    """FormShippingMethods stream class."""

    name = "form_shipping_methods"
    path = "/forms/{form_id}/shipping-methods"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "form_shipping_methods.json"

    parent_stream_type = Forms
    ignore_parent_replication_key = True

    def get_child_context(self, record, context):
        return super().get_child_context(record, context)


class ReturnReasons(ReturnlessStream):
    """ReturnReasons stream class."""

    name = "return_reasons"
    path = "/return-reasons"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "return_reasons.json"


class RequestStatuses(ReturnlessStream):
    """RequestStatuses stream class."""

    name = "request_statuses"
    path = "/request-statuses"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "request_statuses.json"


class ReturnStatuses(ReturnlessStream):
    """ReturnStatuses stream class."""

    name = "return_statuses"
    path = "/return-statuses"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "return_statuses.json"


class RequestOrders(ReturnlessStream):
    """RequestOrders stream class."""

    name = "request_orders"
    path = "/request-orders"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "updated_at"
    schema_filepath = SCHEMAS_DIR / "request_orders.json"

    def get_url_params(self, context, next_page_token):

        params: dict = {
            "include": "customer,form,customer_address,return_question_answers,notes,return_order_items"
        }

        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params


class ReturnOrders(ReturnlessStream):
    """ReturnOrders stream class."""

    name = "return_orders"
    path = "/return-orders"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "updated_at"
    schema_filepath = SCHEMAS_DIR / "return_orders.json"

    def get_url_params(self, context, next_page_token):

        params: dict = {
            "include": "customer,form,customer_address,return_question_answers,notes,shipments"
        }

        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params


class ReturnAddresses(ReturnlessStream):
    """ReturnAddresses stream class."""

    name = "return_addresses"
    path = "/return-addresses"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "return_addresses.json"


class SalesOrders(ReturnlessStream):
    """SalesOrders stream class."""

    name = "sales_orders"
    path = "/sales-orders"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "sales_orders.json"


class Shipments(ReturnlessStream):
    """Shipments stream class."""

    name = "shipments"
    path = "/shipments"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "updated_at"
    schema_filepath = SCHEMAS_DIR / "shipments.json"

    def get_url_params(self, context, next_page_token):

        params: dict = {"include": "customer_address,return_address"}

        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params


class Tags(ReturnlessStream):
    """Tags stream class."""

    name = "tags"
    path = "/tags"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "tags.json"


class Giftcards(ReturnlessStream):
    """Giftcards stream class."""

    name = "giftcards"
    path = "/giftcards"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "giftcards.json"


class Products(ReturnlessStream):
    """Products stream class."""

    name = "products"
    path = "/products"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "products.json"


class Refunds(ReturnlessStream):
    """Refunds stream class."""

    name = "refunds"
    path = "/refunds"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "refunds.json"


class Notes(ReturnlessStream):
    """Notes stream class."""

    name = "notes"
    path = "/notes"
    records_jsonpath = "$.data[*]"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "notes.json"
