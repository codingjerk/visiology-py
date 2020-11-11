"""
Classes and methods to work with ViQube API
"""


from typing import Any, List, Optional, Set

import visiology_py as vi
import i2ls


class Api(vi.BaseApi):
    def __init__(
        self,
        connection: vi.Connection,
        api_version: str,
    ) -> None:
        super().__init__(
            api_prefix="/viqube",
            api_version=api_version,
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

    def post_databases_query(
        self,
        database_unique_identifier: str,
        query: Any,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "POST",
            "/databases/{}/query".format(
                database_unique_identifier,
            ),
            json=query,
            token=token,
        )

    def get_databases_tables(
        self,
        database_unique_identifier: str,
        table_unique_identifier: Optional[str] = None,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        table_modifier = ""
        if table_unique_identifier is not None:
            table_modifier = "/" + table_unique_identifier

        return self._authorized_request(
            "GET",
            "/databases/{}/tables{}".format(
                database_unique_identifier,
                table_modifier,
            ),
            json=None,
            token=token,
        )

    def get_databases_tables_records(
        self,
        database_unique_identifier: str,
        table_unique_identifier: str,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            "/databases/{}/tables/{}/records".format(
                database_unique_identifier,
                table_unique_identifier,
            ),
            json=None,
            token=token,
        )

    def post_databases_tables_records(
        self,
        database_unique_identifier: str,
        table_unique_identifier: str,
        records: List[List[Any]],
        columns: Optional[List[str]] = None,
        chunk_size: int = 100,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        # TODO: move chunk splitting to higher level api wrapper
        results = []
        for chunk in i2ls.chunks(records, chunk_size):
            query: Any = {"values": chunk}
            if columns is not None:
                query["columns"] = columns

            results.append(self._authorized_request(
                "POST",
                "/databases/{}/tables/{}/records".format(
                    database_unique_identifier,
                    table_unique_identifier,
                ),
                json=query,
                token=token,
            ))

        return results

    def delete_databases_tables_records(
        self,
        database_unique_identifier: str,
        table_unique_identifier: str,
        filter: Any = None,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        all_modifier = "/all" if filter is None else ""

        return self._authorized_request(
            "DELETE",
            "/databases/{}/tables/{}/records{}".format(
                database_unique_identifier,
                table_unique_identifier,
                all_modifier,
            ),
            json=filter,
            token=token,
        )

    def get_metadata_databases_dimensions(
        self,
        database_unique_identifier: str,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            "/metadata/databases/{}/dimensions".format(
                database_unique_identifier
            ),
            json=None,
            token=token,
        )

    def get_metadata_databases_measuregroups(
        self,
        database_unique_identifier: str,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            "/metadata/databases/{}/measuregroups".format(
                database_unique_identifier
            ),
            json=None,
            token=token,
        )

    def get_metadata_databases_measuregroups_dimensions(
        self,
        database_unique_identifier: str,
        measuregroup_unique_identifier: str,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            "/metadata/databases/{}/measuregroups/{}/dimensions".format(
                database_unique_identifier,
                measuregroup_unique_identifier,
            ),
            json=None,
            token=token,
        )

    def get_metadata_databases_measuregroups_measures(
        self,
        database_unique_identifier: str,
        measuregroup_unique_identifier: str,
        token: Optional[vi.AuthorizationToken] = None,
    ) -> Any:
        return self._authorized_request(
            "GET",
            "/metadata/databases/{}/measuregroups/{}/measures".format(
                database_unique_identifier,
                measuregroup_unique_identifier,
            ),
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


class ApiV2_5(Api):
    def __init__(self, connection: vi.Connection) -> None:
        super().__init__(connection, api_version="2.5")


class ApiV3(Api):
    def __init__(self, connection: vi.Connection) -> None:
        super().__init__(connection, api_version="3.0")


class Utils:
    @staticmethod
    def find_rawdata_column_id_by_name(
        rawdata: Any,
        column_name: str,
    ) -> Optional[int]:
        for id, column in enumerate(rawdata["columns"]):
            if column["header"] == column_name:
                return id

        return None

    @staticmethod
    def find_rawdata_distinct_values(
        rawdata: Any,
        column_name: str,
    ) -> Set[str]:
        result = set()

        column_id = Utils.find_rawdata_column_id_by_name(rawdata, column_name)

        for row in rawdata["values"]:
            result.add(row[column_id])

        return result
