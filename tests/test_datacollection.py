import visiology_py as vi
import visiology_py.datacollection as dc

from unittest.mock import MagicMock


def test_datacollection_basics() -> None:
    requests = MagicMock()

    connection = vi.Connection(
        schema="https",
        host="whatever.polymedia.ru",
        username="Some user",
        password="Any password",
    )

    api = dc.ApiV2(connection, requests)
