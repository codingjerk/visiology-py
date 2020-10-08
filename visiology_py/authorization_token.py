"""
Common authorization token used for all authorized requests
"""


from dataclasses import dataclass
from datetime import datetime
from typing import Dict


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

    def __str__(self) -> str:
        raise NotImplementedError
