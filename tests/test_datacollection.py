import visiology_py as vi
import visiology_py.datacollection as dc

from typing import Callable, Any
from unittest.mock import Mock, patch
from datetime import datetime
from tests.fixtures import *


def test_datacollection_basics(
    connection: vi.Connection,
) -> None:
    dc.ApiV2(connection)


def test_datacollection_token_emission(
    datacollection_api_v2: dc.ApiV2,
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
        token = datacollection_api_v2.emit_token()

        assert token.type == "Bearer"
        assert token.secret == "SECRET"
        assert token.expires_at == expire_date

    do_test()
