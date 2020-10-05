from tests.fixtures import *
from unittest.mock import patch, Mock

import visiology_py.datacollection as dc
import visiology_py.viqube as vq


def test_datacollection_autoemission(
    requests: Mock,
    datacollection_api_v2: dc.ApiV2,
) -> None:
    @patch(
        "visiology_py.base_api.requests",
        requests,
    )
    def do_test() -> None:
        datacollection_api_v2.get_dimension_elements("dim_Test", {})
        datacollection_api_v2.get_dimension_elements("dim_Test", {})

        calls = [call[0][:2] for call in requests.request.call_args_list]

        assert calls == [
            ("POST", "schema://host/idsrv/connect/token"),
            ("GET", "schema://host/datacollection/api/dimensions/dim_Test/elements?getAll=true"),
            ("GET", "schema://host/datacollection/api/dimensions/dim_Test/elements?getAll=true"),
        ]

    do_test()


def test_viqube_autoemission(
    requests: Mock,
    viqube_api_v3: vq.ApiV3,
) -> None:
    @patch(
        "visiology_py.base_api.requests",
        requests,
    )
    def do_test() -> None:
        viqube_api_v3.post_metadata_rawdata_query({})
        viqube_api_v3.post_metadata_rawdata_query({})

        calls = [call[0][:2] for call in requests.request.call_args_list]

        assert calls == [
            ("POST", "schema://host/idsrv/connect/token"),
            ("POST", "schema://host/viqube/metadata/rawdata/query"),
            ("POST", "schema://host/viqube/metadata/rawdata/query"),
        ]

    do_test()
