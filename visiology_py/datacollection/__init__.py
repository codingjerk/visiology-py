from typing import Any, Optional, Callable, List, Dict
from datetime import datetime, timedelta

import visiology_py as vi
import requests


class ApiV1:
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
        url = f"{schema}://{host}/idsrv/connect/token"

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
        token: vi.AuthorizationToken,
        dimension_id: int,
        filter: dict,
    ) -> dict:
        schema = self.connection.schema
        host = self.connection.host
        response = self.requests.get(
            self.__url(f"/dimensions/{dimension_id}/elements?getAll=true"),
            headers=self.__headers(token),
            json=filter,
        )

        assert response.status_code == 200, response.text
        return response.json()

    def put_dimension_elements(
        self,
        token: vi.AuthorizationToken,
        dimension_id: int,
        elements: List[dict],
    ) -> dict:
        schema = self.connection.schema
        host = self.connection.host
        response = self.requests.put(
            self.__url(f"/dimensions/{dimension_id}/elements"),
            headers=self.__headers(token),
            json=elements,
        )

        assert response.status_code == 200, response.text
        return response.json()

    def post_dimension_elements(
        self,
        token: vi.AuthorizationToken,
        dimension_id: int,
        elements: List[dict],
    ) -> dict:
        response = self.requests.post(
            self.__url(f"/dimensions/{dimension_id}/elements"),
            headers=self.__headers(token),
            json=elements,
        )

        assert response.status_code == 200, response.text
        return response.json()

    def delete_dimension_elements(
        self,
        token: vi.AuthorizationToken,
        dimension_id: int,
        filter: List[dict],
    ) -> dict:
        response = self.requests.delete(
            self.__url(f"/dimensions/{dimension_id}/elements"),
            headers=self.__headers(token),
            json=filter,
        )

        assert response.status_code == 200, response.text
        return response.json()

    def __headers(self, token: vi.AuthorizationToken) -> Dict[str, str]:
        return {
            "Authorization": f"{token.type} {token.secret}",
            "Content-Type": "application/json",
            "X-API-VERSION": "1.0",
        }

    def __url(self, path: str) -> str:
        schema = self.connection.schema
        host = self.connection.host
        return f"{schema}://{host}/datacollection/api{path}"


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
            "openid",
            "profile",
            "email",
            "roles",
            "viewer_api",
            "core_logic_facade",
        ]
        schema = self.connection.schema
        host = self.connection.host
        url = f"{schema}://{host}/idsrv/connect/token"

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
        token: vi.AuthorizationToken,
        dimension_unique_name: str,
        filter: dict,
    ) -> dict:
        schema = self.connection.schema
        host = self.connection.host
        response = self.requests.get(
            self.__url(f"/dimensions/{dimension_unique_name}/elements?getAll=true"),
            headers=self.__headers(token),
            json=filter,
        )

        assert response.status_code == 200, response.text
        return response.json()

    def put_dimension_elements(
        self,
        token: vi.AuthorizationToken,
        dimension_unique_name: str,
        elements: List[dict],
    ) -> dict:
        schema = self.connection.schema
        host = self.connection.host
        response = self.requests.put(
            self.__url(f"/dimensions/{dimension_unique_name}/elements"),
            headers=self.__headers(token),
            json=elements,
        )

        assert response.status_code == 200, response.text
        return response.json()

    def post_dimension_elements(
        self,
        token: vi.AuthorizationToken,
        dimension_unique_name: str,
        elements: List[dict],
    ) -> dict:
        response = self.requests.post(
            self.__url(f"/dimensions/{dimension_unique_name}/elements"),
            headers=self.__headers(token),
            json=elements,
        )

        assert response.status_code == 200, response.text
        return response.json()

    def delete_dimension_elements(
        self,
        token: vi.AuthorizationToken,
        dimension_unique_name: str,
        filter: List[dict],
    ) -> dict:
        response = self.requests.delete(
            self.__url(f"/dimensions/{dimension_unique_name}/elements"),
            headers=self.__headers(token),
            json=filter,
        )

        assert response.status_code == 200, response.text
        return response.json()

    def __headers(self, token: vi.AuthorizationToken) -> Dict[str, str]:
        return {
            "Authorization": f"{token.type} {token.secret}",
            "Content-Type": "application/json",
            "X-API-VERSION": "2.0",
        }

    def __url(self, path: str) -> str:
        schema = self.connection.schema
        host = self.connection.host
        return f"{schema}://{host}/datacollection/api{path}"


class Utils:
    @staticmethod
    def find_attribute_by_unique_name(
        dimension_element: dict,
        attribute_unique_name: dict,
    ) -> Optional[dict]:
        for attribute in dimension_element:
            if attribute["attributeId"] == attribute_unique_name:
                return attribute

    @staticmethod
    def find_dimension_element_by_predicate(
        dimension_elements: dict,
        predicate: Callable[[dict], bool],
    ) -> Optional[dict]:
        for element in dimension_elements["elements"]:
            if predicate(element):
                return element

    @staticmethod
    def find_dimension_element_by_attribute(
        dimension_elements: dict,
        attribute_unique_name: str,
        attribute_value: str
    ) -> Optional[dict]:
        def predicate(element):
            attribute = Utils.find_attribute_by_unique_name(element, attribute_unique_name)
            return attribute is not None and attribute["value"] == attribute_value

        return Utils.find_dimension_element_by_predicate(dimension_elements, predicate)

    @staticmethod
    def find_dimension_element_by_name(
        dimension_elements: dict,
        element_name: str,
    ) -> Optional[dict]:
        def predicate(element):
            return element["name"] == element_name

        return Utils.find_dimension_element_by_predicate(dimension_elements, predicate)

    @staticmethod
    def find_dimension_element_by_id(
        dimension_elements: dict,
        element_id: int,
    ) -> Optional[dict]:
        def predicate(element):
            return element["id"] == element_id

        return Utils.find_dimension_element_by_predicate(dimension_elements, predicate)

    @staticmethod
    def prepare_dimension_element_to_insert(
        dimension_element: dict,
        attribute_map: dict,
    ) -> None:
        for attribute in dimension_element["attributes"]:
            attribute_id = attribute["attributeId"]
            if attribute_id in attribute_map:
                attribute["value"] = attribute_map[attribute_id]
