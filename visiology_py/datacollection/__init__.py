from typing import Any, Optional
from datetime import datetime, timedelta

import visiology_py as vi
import requests


class ApiV2:
    def __init__(
        self,
        connection: vi.Connection,
        requests: Any = requests
    ) -> None:
        self.connection = connection
        self.requests = requests

    def emit_token(
        self,
        emission_date: Optional[datetime] = None
    ) -> vi.AuthorizationToken:
        if emission_date is None:
            emission_date = datetime.now()

        scopes = [
            "openid", "profile", "email",
            "roles", "viewer_api", "core_logic_facade",
        ]
        schema = self.connection.schema
        host = self.connection.host
        url = f"{schema}://{host}/idsrv/connect/token",

        response = self.requests.post(
            url,
            headers={
                "Authorization": "Basic cm8uY2xpZW50OmFtV25Cc3B9dipvfTYkSQ==",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "password",
                "scope": " ".join(scopes),
                "response_type": "id_token token",
                "username": self.connection.username,
                "password": self.connection.password,
            },
        )

        token = response.json()
        expires_in = token["expires_in"]
        expires_at = emission_date + timedelta(seconds=expires_in)

        return vi.AuthorizationToken(
            type=token["token_type"],
            secret=token["access_token"],
            expires_at=expires_at,
        )

    def get_dimension_elements(
        self,
        token: AuthorizationToken,
        dimension_unique_name: str,
        filter: dict,
    ) -> dict:
        response = self.requests.get(
            f"{schema}://{host}/datacollection/api/dimensions/{dimension_unique_name}/elements?getAll=true",
            headers={
                "Authorization": f"{token.type} {token.secret}",
                "Content-Type": "application/json",
                "X-API-VERSION": "2.0",
            },
            json=filter,
        )
