import pytest
from tests import fakes
from tests.fixtures import *
from unittest.mock import patch, Mock


def test_datacollection_autoemission(
    requests: Mock,
) -> None:
    @patch(
        "visiology_py.base_api.requests",
        requests,
    )
    def do_test() -> None:
        api = fakes.datacollection_api_v2()

        api.get_dimension_elements("dim_Test", {})
        api.get_dimension_elements("dim_Test", {})

        calls = [call[0][:2] for call in requests.request.call_args_list]

        assert calls == [
            ("POST", "schema://host/idsrv/connect/token"),
            ("GET", "schema://host/datacollection/api/dimensions/dim_Test/elements?getAll=true"),
            ("GET", "schema://host/datacollection/api/dimensions/dim_Test/elements?getAll=true"),
        ]

    do_test()


def test_viqube_autoemission(
    requests: Mock,
) -> None:
    @patch(
        "visiology_py.base_api.requests",
        requests,
    )
    def do_test() -> None:
        api = fakes.viqube_api_v3()

        api.post_metadata_rawdata_query({})
        api.post_metadata_rawdata_query({})

        calls = [call[0][:2] for call in requests.request.call_args_list]

        assert calls == [
            ("POST", "schema://host/idsrv/connect/token"),
            ("POST", "schema://host/viqube/metadata/rawdata/query"),
            ("POST", "schema://host/viqube/metadata/rawdata/query"),
        ]

    do_test()
