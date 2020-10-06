from datetime import timedelta
from unittest.mock import Mock

from visiology_py.decorators import cached


def test_cached_caches_calls() -> None:
    function = Mock()

    cached_function = cached(time_to_live=timedelta(seconds=1))(function)
    cached_function()
    cached_function()

    function.assert_called_once()


def test_cached_do_not_mix_calls() -> None:
    function = Mock()

    cached_function = cached(time_to_live=timedelta(seconds=1))(function)
    cached_function(1)
    cached_function(2)

    assert function.call_count == 2
