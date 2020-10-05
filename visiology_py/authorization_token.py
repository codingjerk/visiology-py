"""
Common authorization token used for all authorized requests
"""


from dataclasses import dataclass
from typing import Dict
from datetime import datetime


@dataclass
class AuthorizationToken:
    type: str
    secret: str
    expires_at: datetime

    def is_expired(self) -> bool:
        return datetime.now() >= self.expires_at

    def to_authorization_header(self) -> Dict[str, str]:
        return {
            "Authorization": f"{self.type} {self.secret}",
        }
