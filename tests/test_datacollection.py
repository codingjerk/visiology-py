import visiology_py as vi
import visiology_py.datacollection as dc

from typing import Callable, Any
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from tests.fixtures import *


test_connection = vi.Connection(
    schema="https",
    host="whatever.polymedia.ru",
    username="Some user",
    password="Any password",
)


def test_datacollection_basics() -> None:
    api = dc.ApiV2(test_connection)


def test_datacollection_token_emission(
    emission_date: datetime,
    expire_date: datetime,
    fixed_datetime: Callable[[datetime], Mock],
    requests: Any,
) -> None:
    @patch(
        "visiology_py.base_api.requests",
        requests,
    )
    @patch(
        "visiology_py.base_api.datetime",
        fixed_datetime(emission_date),
    )
    def do_test() -> None:
        api = dc.ApiV2(test_connection)

        token = api.emit_token()

        assert token.type == "Bearer"
        assert token.secret == "SECRET"
        assert token.expires_at == expire_date

    do_test()
