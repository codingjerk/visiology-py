import visiology_py as vi
import visiology_py.datacollection as dc

from typing import Callable
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
    requests = Mock()
    api = dc.ApiV2(test_connection, requests)


def test_datacollection_token_emission(
    expires_in: timedelta,
    emission_date: datetime,
    expire_date: datetime,
    fixed_datetime: Callable[[datetime], Mock],
) -> None:
    requests = Mock()
    requests.post = Mock()
    requests.request().json = Mock(return_value={
        "token_type": "Bearer",
        "access_token": "SECRET",
        "expires_in": expires_in.total_seconds(),
    })

    api = dc.ApiV2(test_connection, requests)

    with patch(
        "visiology_py.base_api.datetime",
        fixed_datetime(emission_date),
    ):
        token = api.emit_token()

        assert token.type == "Bearer"
        assert token.secret == "SECRET"
        assert token.expires_at == expire_date
