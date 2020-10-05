from typing import Any

import visiology_py.datacollection as dc
import visiology_py.viqube as vq
import visiology_py as vi
from unittest.mock import MagicMock


def datacollection_api_v2(**kwargs: Any) -> dc.ApiV2:
    if "connection" not in kwargs:
        kwargs["connection"] = connection()

    return dc.ApiV2(**kwargs)


def viqube_api_v3(**kwargs: Any) -> vq.ApiV3:
    if "connection" not in kwargs:
        kwargs["connection"] = connection()

    return vq.ApiV3(**kwargs)


def connection() -> vi.Connection:
    return vi.Connection(
        schema="schema",
        host="host",
        username="username",
        password="password",
    )


def requests(returns_token: bool = False) -> MagicMock:
    response = MagicMock()
    response.status_code = 200
    response.json = MagicMock(return_value={
        "expires_in": 1000,
        "token_type": "Bearer",
        "access_token": "SECRET",
    })

    requests = MagicMock()
    requests.request = MagicMock(return_value=response)

    return requests
