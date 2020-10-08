from datetime import timedelta
from unittest.mock import Mock

import visiology_py.datacollection as dc
from visiology_py.decorators import cached, retried, decorate_api


def exp(x: int) -> float:
    return float(0.1 * (2 ** x))


decorate_api(
    dc.ApiV2,
    retried(max_tries=1, timeout_function=exp),
)


def test_cached_caches_calls() -> None:
    function = Mock()
    function.__name__ = "get_dimension_attributes"

    cached_function = cached(time_to_live=timedelta(seconds=1))(function)
    cached_function()
    cached_function()

    function.assert_called_once()


def test_cached_do_not_mix_calls() -> None:
    function = Mock()
    function.__name__ = "get_dimension_elements"

    cached_function = cached(time_to_live=timedelta(seconds=1))(function)
    cached_function("self", 1)
    cached_function("self", 2)

    assert function.call_count == 2
