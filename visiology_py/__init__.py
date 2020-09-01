from typing import NamedTuple
from datetime import datetime


class Connection(NamedTuple):
    schema: str
    host: str
    username: str
    password: str


class AuthorizationToken(NamedTuple):
    type: str
    secret: str
    expires_at: datetime
