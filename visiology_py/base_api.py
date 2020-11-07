"""
Base API class including methods shared between all APIs
"""


from datetime import datetime, timedelta
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, Optional
from json.decoder import JSONDecodeError

import requests

from visiology_py.authorization_token import AuthorizationToken
from visiology_py.connection import Connection


class TokenEmissionError(Exception):
    def __init__(self, status_code: int, response_text: str) -> None:
        message = (
            f'server returned "bad" status code ({status_code}) '
            f'with response text "{response_text}"'
        )
        super().__init__(message)


class BaseApi:
    def __init__(
        self,
        api_prefix: str,
        api_version: str,
        authorization_scopes: List[str],
        authorization_headers: Dict[str, str],
        connection: Connection,
    ) -> None:
        self._api_prefix = api_prefix
        self._api_version = api_version
        self._authorization_scopes = authorization_scopes
        self._authorization_headers = authorization_headers
        self._connection = connection

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
    ) -> AuthorizationToken:
        response = requests.request(
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

        if response.status_code != 200:
            raise TokenEmissionError(response.status_code, response.text)

        try:
            token = response.json()
        except Exception:
            raise TokenEmissionError(
                response.status_code,
                response.text
            ) from None

        if any(
            [
                "expires_in" not in token,
                "token_type" not in token,
                "access_token" not in token,
            ]
        ):
            raise TokenEmissionError(response.status_code, response.text)

        expires_in = token["expires_in"]
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        return AuthorizationToken(
            type=token["token_type"],
            secret=token["access_token"],
            expires_at=expires_at,
        )

    def _ensure_token(
        self,
    ) -> AuthorizationToken:
        if self._token is None or self._token.is_expired():
            self._token = self.emit_token()

        return self._token

    def _authorized_request(
        self,
        method: str,
        path: str,
        json: Any,
        token: Optional[AuthorizationToken] = None,
    ) -> Any:
        if token is None:
            token = self._ensure_token()

        # TODO: specify timeout and use scaling timeout
        response = requests.request(
            method,
            self._prefixed_url(path),
            headers=self._headers(token),
            json=json,
        )

        assert response.status_code == 200, response.text

        try:
            return response.json()
        except JSONDecodeError:
            assert response.text == "", response.text
