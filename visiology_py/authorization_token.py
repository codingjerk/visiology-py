"""
Common authorization token used for all authorized requests
"""


from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime


@dataclass
class AuthorizationToken:
    type: str
    secret: str
    expires_at: datetime

    def is_expired(self, at_date: Optional[datetime]) -> bool:
        if at_date is None:
            at_date = datetime.now()

        return at_date >= self.expires_at

    def to_authorization_header(self) -> Dict[str, str]:
        return {
            "Authorization": f"{self.type} {self.secret}",
        }
