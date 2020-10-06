from datetime import datetime
from typing import Callable
from unittest.mock import Mock, patch

import visiology_py as vi
from tests.fixtures import *


def test_token_expires(
    expire_date: datetime,
    before_expire_date: datetime,
    after_expire_date: datetime,
    fixed_datetime: Callable[[datetime], Mock],
) -> None:
    token = vi.AuthorizationToken(
        type="Something",
        secret="Anything",
        expires_at=expire_date,
    )

    with patch(
        "visiology_py.authorization_token.datetime",
        fixed_datetime(after_expire_date),
    ):
        assert token.is_expired()

    with patch(
        "visiology_py.authorization_token.datetime",
        fixed_datetime(before_expire_date),
    ):
        assert not token.is_expired()
