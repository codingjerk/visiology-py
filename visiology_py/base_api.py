"""
Base API class including methods shared between all APIs
"""


from typing import Any, Optional, List, Dict
from datetime import datetime, timedelta

from visiology_py.connection import Connection
from visiology_py.authorization_token import AuthorizationToken


class BaseApi:
    def __init__(
        self,
        api_prefix: str,
        api_version: str,
        authorization_scopes: List[str],
        authorization_headers: Dict[str, str],
        connection: Connection,
        requests: Any,
    ) -> None:
        self._api_prefix = api_prefix
        self._api_version = api_version
        self._authorization_scopes = authorization_scopes
        self._authorization_headers = authorization_headers
        self._connection = connection
        self._requests = requests

        self._token: Optional[AuthorizationToken] = None

    def _url(self, path: str) -> str:
        schema = self._connection.schema
        host = self._connection.host

        return f"{schema}://{host}{path}"

    def _prefixed_url(self, path: str) -> str:
        return self._url(f"{self._api_prefix}{path}")

    def _headers(self, token: AuthorizationToken) -> Dict[str, str]:
        return {
            **token.to_authorization_header(),
            "Content-Type": "application/json",
            "X-API-VERSION": self._api_version,
        }

    def emit_token(
        self,
        emission_date: Optional[datetime] = None,
    ) -> AuthorizationToken:
        if emission_date is None:
            emission_date = datetime.now()

        response = self._requests.request(
            "POST",
            self._url("/idsrv/connect/token"),
            headers=self._authorization_headers,
            data={
                "grant_type": "password",
                "scope": " ".join(self._authorization_scopes),
                "response_type": "id_token token",
                "username": self._connection.username,
                "password": self._connection.password,
            },
        )

        token = response.json()
        expires_in = token["expires_in"]
        expires_at = emission_date + timedelta(seconds=expires_in)

        return AuthorizationToken(
            type=token["token_type"],
            secret=token["access_token"],
            expires_at=expires_at,
        )

    def _ensure_token(
        self,
        at_date: Optional[datetime],
    ) -> AuthorizationToken:
        if self._token is None or self._token.is_expired(at_date):
            self._token = self.emit_token(at_date)

        return self._token

    def _authorized_request(
        self,
        method: str,
        path: str,
        json: Any,
        token: Optional[AuthorizationToken] = None,
        at_date: Optional[datetime] = None,
    ) -> Any:
        if token is None:
            token = self._ensure_token(at_date)

        response = self._requests.request(
            method,
            self._prefixed_url(path),
            headers=self._headers(token),
            json=json,
        )

        assert response.status_code == 200, response.text
        return response.json()
