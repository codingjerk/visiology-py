"""
Classes and methods to work with ViQube API
"""


from typing import Any, Optional, Set

import visiology_py as vi


class ApiV3(vi.BaseApi):
    def __init__(
        self,
        connection: vi.Connection,
    ) -> None:
        super().__init__(
            api_prefix="/viqube",
            api_version="3.0",
            authorization_scopes=[
                "openid",
                "profile",
                "email",
                "roles",
                "viqubeadmin_api",
                "viqube_api",
            ],
            authorization_headers={
                "Authorization": (
                    "Basic "
                    "dmlxdWJlYWRtaW5fcm9fY2xpZW50OjcmZEo1UldwVVMkLUVVQE1reHU="
                ),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            connection=connection,
        )

    def get_metadata_databases_measuregroups(
        self,
        database_unique_identifier: str,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            f"/metadata/databases/{database_unique_identifier}/measuregroups",
            json=None,
            token=token,
        )

    def post_metadata_rawdata_query(
        self,
        query: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "POST",
            "/metadata/rawdata/query",
            json=query,
            token=token,
        )

    def version(
        self,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            "/version",
            json=None,
            token=token,
        )


class Utils:
    def find_rawdata_column_id_by_name(
        rawdata: Any,
        column_name: str,
    ) -> Optional[int]:
        for id, column in enumerate(rawdata["columns"]):
            if column["header"] == column_name:
                return id

        return None

    def find_rawdata_distinct_values(
        rawdata: Any,
        column_name: str,
    ) -> Set[str]:
        result = set()

        column_id = Utils.find_rawdata_column_id_by_name(rawdata, column_name)

        for row in rawdata["values"]:
            result.add(row[column_id])

        return result
