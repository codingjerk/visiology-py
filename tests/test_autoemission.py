from tests import fakes


def test_datacollection_autoemission() -> None:
    requests = fakes.requests(returns_token=True)
    api = fakes.datacollection_api_v2(requests=requests)

    api.get_dimension_elements("dim_Test", {})
    api.get_dimension_elements("dim_Test", {})

    calls = [call.args[:2] for call in requests.request.call_args_list]

    assert calls == [
        ("POST", "schema://host/idsrv/connect/token"),
        ("GET", "schema://host/datacollection/api/dimensions/dim_Test/elements?getAll=true"),
        ("GET", "schema://host/datacollection/api/dimensions/dim_Test/elements?getAll=true"),
    ]

def test_viqube_autoemission() -> None:
    requests = fakes.requests(returns_token=True)
    api = fakes.viqube_api_v3(requests=requests)

    api.post_metadata_rawdata_query({})
    api.post_metadata_rawdata_query({})

    calls = [call.args[:2] for call in requests.request.call_args_list]

    assert calls == [
        ("POST", "schema://host/idsrv/connect/token"),
        ("POST", "schema://host/viqube/metadata/rawdata/query"),
        ("POST", "schema://host/viqube/metadata/rawdata/query"),
    ]
