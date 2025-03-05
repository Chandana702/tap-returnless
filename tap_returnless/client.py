"""REST client handling, including ReturnlessStream base class."""

from __future__ import annotations

import typing as t
from importlib import resources
from datetime import datetime

from singer_sdk.authenticators import BearerTokenAuthenticator
from urllib.parse import parse_qsl, urlparse, ParseResult
from singer_sdk.pagination import BaseHATEOASPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"


class MyPaginator(BaseHATEOASPaginator):
    def get_next_url(self, response):
        data = response.json()
        next_url = data.get("links", {}).get("next")
        return next_url


class ReturnlessStream(RESTStream):
    """Returnless stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config
        return "https://api-v2.returnless.com/2023-01"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("auth_token", ""),
        )

    def get_new_paginator(self):
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return MyPaginator()

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            # Check if next_page_token is already parsed
            if isinstance(next_page_token, ParseResult):
                parsed_url = next_page_token  # Already parsed
            else:
                parsed_url = urlparse(next_page_token)  # Parse if it's a string

            params.update(parse_qsl(parsed_url.query))

        return params

    def post_process(
        self,
        row: dict,
        context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        start_date = self.config.get("start_date")
        # start_date = "2025-01-01"

        if not start_date:
            return row

        updated_at_str = row.get("updated_at")
        if not updated_at_str:
            return row

        # Append time part to start_date and convert to datetime
        start_date_dt = datetime.fromisoformat(f"{start_date}T00:00:00+00:00")

        # Convert updated_at to datetime (automatically handles timezone)
        updated_at_dt = datetime.fromisoformat(updated_at_str)

        return row if updated_at_dt >= start_date_dt else None
