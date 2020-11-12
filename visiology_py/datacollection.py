"""
Classes and methods to work with DataCollection API
"""


from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

import visiology_py as vi


EntityId = TypeVar("EntityId")


class Api(vi.BaseApi, Generic[EntityId]):
    def __init__(
        self,
        connection: vi.Connection,
        api_version: str,
    ) -> None:
        super().__init__(
            api_prefix="/datacollection/api",
            api_version=api_version,
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
        dimension_id: EntityId,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            f"/dimensions/{dimension_id}/attributes?getAll=true",
            json=None,
            token=token,
        )

    # TODO: make filter optional
    def get_dimension_elements(
        self,
        dimension_id: EntityId,
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
        dimension_id: EntityId,
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
        dimension_id: EntityId,
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
        dimension_id: EntityId,
        filter: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "DELETE",
            f"/dimensions/{dimension_id}/elements",
            json=filter,
            token=token,
        )

    def get_measuregroups(
        self,
        measuregroup_id: Optional[EntityId] = None,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        modifier = "?getAll=true"
        if measuregroup_id is not None:
            modifier = f"/{measuregroup_id}"

        return self._authorized_request(
            "GET",
            f"/measuregroups{modifier}",
            json=None,
            token=token,
        )

    def get_measuregroups_elements(
        self,
        measuregroup_id: EntityId,
        filter: Any = None,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            f"/measuregroups/{measuregroup_id}/elements?getAll=true",
            json=filter,
            token=token,
        )

    def post_measuregroups_elements(
        self,
        measuregroup_id: EntityId,
        elements: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "POST",
            f"/measuregroups/{measuregroup_id}/elements",
            json=elements,
            token=token,
        )

    # TODO: use name consistent with api
    def get_measure_group_forms(
        self,
        measuregroup_id: EntityId,
        filter: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            f"/measuregroups/{measuregroup_id}/forms",
            json=filter,
            token=token,
        )


class ApiV1(Api[int]):
    def __init__(self, connection: vi.Connection):
        super().__init__(connection, api_version="1.0")


class ApiV2(Api[str]):
    def __init__(self, connection: vi.Connection):
        super().__init__(connection, api_version="2.0")


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
