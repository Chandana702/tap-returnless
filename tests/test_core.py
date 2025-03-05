"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_returnless.tap import TapReturnless

SAMPLE_CONFIG = {
    # "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "start_date": "2025-01-01",
    "auth_token": "d1s462Ug8eBE81QiBzO2V1GJEUutE2Qf6AhHJkHP85ce2967",
    # TODO: Initialize minimal tap config
}


# Run standard built-in tap tests from the SDK:
TestTapReturnless = get_tap_test_class(
    tap_class=TapReturnless,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
