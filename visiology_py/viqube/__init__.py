from typing import Any, Optional
from datetime import datetime, timedelta

import visiology_py as vi
import requests


class ApiV3:
    def __init__(
        self,
        connection: vi.Connection,
        requests: Any = requests,
    ) -> None:
        self.connection = connection
        self.requests = requests

    def emit_token(
        self,
        emission_date: Optional[datetime] = None,
    ) -> vi.AuthorizationToken:
        if emission_date is None:
            emission_date = datetime.now()

        scopes = [
            "openid", "profile", "email", "roles",
            "viqubeadmin_api", "viqube_api",
        ]
        schema = self.connection.schema
        host = self.connection.host
        url = f"{schema}://{host}/idsrv/connect/token"

        response = self.requests.post(
            url,
            headers={
                "Authorization":
                    "Basic "
                    "dmlxdWJlYWRtaW5fcm9fY2xpZW50OjcmZEo1UldwVVMkLUVVQE1reHU=",
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

    def version(self, token: vi.AuthorizationToken) -> Any:
        schema = self.connection.schema
        host = self.connection.host
        url = f"{schema}://{host}/viqube/version"

        response = requests.get(
            url,
            headers={
                "Authorization": f"{token.type} {token.secret}",
                "Content-Type": "application/json",
                "X-API-VERSION": "3.0",
            },
        )

        assert response.status_code == 200, response.text
        return response.json()

    def post_metadata_rawdata_query(
        self,
        token: vi.AuthorizationToken,
        query: Any,
    ) -> Any:
        schema = self.connection.schema
        host = self.connection.host
        url = f"{schema}://{host}/viqube/metadata/rawdata/query"

        response = requests.post(
            url,
            headers={
                "Authorization": f"{token.type} {token.secret}",
                "Content-Type": "application/json",
                "X-API-VERSION": "3.0",
            },
            json=query,
        )

        assert response.status_code == 200, response.text
        return response.json()
