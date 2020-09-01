import visiology_py as vi
from datetime import datetime, timedelta


def test_token_expires() -> None:
    emission_date = datetime(2020, 1, 2, 3, 4, 5)
    token = vi.AuthorizationToken(
        type="Something",
        secret="Anything",
        expires_at=emission_date + timedelta(seconds=10),
    )

    assert token.is_expired(at_date=emission_date + timedelta(seconds=20))
    assert not token.is_expired(at_date=emission_date + timedelta(seconds=5))
