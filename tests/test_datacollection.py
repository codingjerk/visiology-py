import visiology_py as vi
import visiology_py.datacollection as dc

from unittest.mock import MagicMock
from datetime import datetime


test_connection = vi.Connection(
    schema="https",
    host="whatever.polymedia.ru",
    username="Some user",
    password="Any password",
)


def test_datacollection_basics() -> None:
    requests = MagicMock()
    api = dc.ApiV2(test_connection, requests)


def test_datacollection_token_emission() -> None:
    requests = MagicMock()
    requests.post = MagicMock()
    requests.post().json = MagicMock(return_value={
        "token_type": "Bearer",
        "access_token": "SECRET",
        "expires_in": 10,
    })

    emission_date = datetime(year=2020, month=3, day=20, hour=13, minute=31, second=20)

    api = dc.ApiV2(test_connection, requests)
    token = api.emit_token(emission_date)

    assert token.type == "Bearer"
    assert token.secret == "SECRET"
    assert token.expires_at == emission_date + timedelta(seconds=10)
