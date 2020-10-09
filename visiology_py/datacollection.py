"""
Classes and methods to work with DataCollection API
"""


from typing import Any, Callable, Dict, List, Optional

import visiology_py as vi


class ApiV1(vi.BaseApi):
    def __init__(
        self,
        connection: vi.Connection,
    ) -> None:
        super().__init__(
            api_prefix="/datacollection/api",
            api_version="1.0",
            authorization_scopes=[
                "openid",
                "profile",
                "email",
                "roles",
                "viewer_api",
                "core_logic_facade",
            ],
            authorization_headers={
                "Authorization": "Basic cm8uY2xpZW50OmFtV25Cc3B9dipvfTYkSQ==",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            connection=connection,
        )

    def get_dimension_attributes(
        self,
        dimension_id: int,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            f"/dimensions/{dimension_id}/attributes?getAll=true",
            json=None,
            token=token,
        )

    def get_dimension_elements(
        self,
        dimension_id: int,
        filter: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            f"/dimensions/{dimension_id}/elements?getAll=true",
            json=filter,
            token=token,
        )

    def put_dimension_elements(
        self,
        dimension_id: int,
        elements: List[Any],
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "PUT",
            f"/dimensions/{dimension_id}/elements",
            json=elements,
            token=token,
        )

    def post_dimension_elements(
        self,
        dimension_id: int,
        elements: List[Any],
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "POST",
            f"/dimensions/{dimension_id}/elements",
            json=elements,
            token=token,
        )

    def delete_dimension_elements(
        self,
        dimension_id: int,
        filter: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "DELETE",
            f"/dimensions/{dimension_id}/elements",
            json=filter,
            token=token,
        )


class ApiV2(vi.BaseApi):
    def __init__(
        self,
        connection: vi.Connection,
    ) -> None:
        super().__init__(
            api_prefix="/datacollection/api",
            api_version="2.0",
            authorization_scopes=[
                "openid",
                "profile",
                "email",
                "roles",
                "viewer_api",
                "core_logic_facade",
            ],
            authorization_headers={
                "Authorization": "Basic cm8uY2xpZW50OmFtV25Cc3B9dipvfTYkSQ==",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            connection=connection,
        )

    def get_dimension_attributes(
        self,
        dimension_unique_name: str,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            f"/dimensions/{dimension_unique_name}/attributes?getAll=true",
            json=None,
            token=token,
        )

    def get_dimension_elements(
        self,
        dimension_unique_name: str,
        filter: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            f"/dimensions/{dimension_unique_name}/elements?getAll=true",
            json=filter,
            token=token,
        )

    def put_dimension_elements(
        self,
        dimension_unique_name: str,
        elements: List[Any],
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "PUT",
            f"/dimensions/{dimension_unique_name}/elements",
            json=elements,
            token=token,
        )

    def post_dimension_elements(
        self,
        dimension_unique_name: str,
        elements: List[Any],
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "POST",
            f"/dimensions/{dimension_unique_name}/elements",
            json=elements,
            token=token,
        )

    def delete_dimension_elements(
        self,
        dimension_unique_name: str,
        filter: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "DELETE",
            f"/dimensions/{dimension_unique_name}/elements",
            json=filter,
            token=token,
        )

    def get_measure_group_forms(
        self,
        measure_group_unique_name: str,
        filter: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            f"/measuregroups/{measure_group_unique_name}/forms",
            json=filter,
            token=token,
        )


class Utils:
    @staticmethod
    def find_attribute_by_unique_name(
        dimension_element: Any,
        attribute_unique_name: str,
    ) -> Any:
        for attribute in dimension_element["attributes"]:
            if attribute["attributeId"] == attribute_unique_name:
                return attribute

    @staticmethod
    def find_dimension_element_by_predicate(
        dimension_elements: Any,
        predicate: Callable[[Any], bool],
    ) -> Any:
        for element in dimension_elements["elements"]:
            if predicate(element):
                return element

    @staticmethod
    def find_dimension_element_by_attribute(
        dimension_elements: Any,
        attribute_unique_name: str,
        attribute_value: str
    ) -> Any:
        def predicate(element: Dict[str, Any]) -> bool:
            attribute = Utils.find_attribute_by_unique_name(
                element,
                attribute_unique_name,
            )
            return all((
                attribute is not None,
                attribute["value"] == attribute_value,
            ))

        return Utils.find_dimension_element_by_predicate(
            dimension_elements,
            predicate,
        )

    @staticmethod
    def find_dimension_element_by_name(
        dimension_elements: Any,
        element_name: str,
    ) -> Any:
        def predicate(element: Dict[str, Any]) -> bool:
            return bool(element["name"] == element_name)

        return Utils.find_dimension_element_by_predicate(
            dimension_elements,
            predicate,
        )

    @staticmethod
    def find_dimension_element_by_id(
        dimension_elements: Any,
        element_id: int,
    ) -> Any:
        def predicate(element: Dict[str, Any]) -> bool:
            return bool(element["id"] == element_id)

        return Utils.find_dimension_element_by_predicate(
            dimension_elements,
            predicate,
        )

    @staticmethod
    def prepare_dimension_element_to_insert(
        dimension_element: Any,
        attribute_map: Dict[str, Any],
    ) -> None:
        for attribute in dimension_element["attributes"]:
            attribute_id = attribute["attributeId"]
            if attribute_id in attribute_map:
                attribute["value"] = attribute_map[attribute_id]
