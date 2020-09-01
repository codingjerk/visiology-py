from typing import NamedTuple, Optional
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

    def is_expired(self, at_date: Optional[datetime]) -> bool:
        if at_date is None:
            at_date = datetime.now()

        return at_date >= self.expires_at
