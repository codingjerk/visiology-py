import pytest
from hypothesis import given
import tests.strategies as st
from typing import Any, Collection, List, TypeVar

import i2ls


T = TypeVar("T")


@given(st.anything())
def test_make_hashable_properties(a: Any) -> None:
    assert hash(i2ls.make_hashable(a)) is not None


def test_make_hashable_unknown_types() -> None:
    class Unhashable:
        __hash__ = None  # type: ignore

    with pytest.raises(NotImplementedError):
        i2ls.make_hashable(Unhashable())


@given(st.anything_iterable())
def test_duplicates_properties(xs: Collection[T]) -> None:
    dups = list(i2ls.duplicates(xs))

    assert len(dups) <= len(xs)

    for item in dups:
        assert list(xs).count(item) > 1


def test_duplicates_simple() -> None:
    dups1 = list(i2ls.duplicates([1, 2, 3]))
    assert dups1 == []

    dups2 = list(i2ls.duplicates([1, 1, 2, 3, 4, 4, 5]))
    assert dups2 == [1, 4]

    dups3 = list(i2ls.duplicates([{1: 2}, {3: 4}, {1: 2}, [5, 6], {7, 8}], hash=i2ls.make_hashable))
    assert dups3 == [{1: 2}]

    dups4 = list(i2ls.duplicates([1, 1, 2, 3, 4, 4, 5, 4, 6]))
    assert dups4 == [1, 4]


def test_chunks_splits_empty_iterables() -> None:
    data: List[int] = []
    result = list(i2ls.chunks(data, size=2))

    assert result == []


def test_chunks_splits_without_tail() -> None:
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    result = list(i2ls.chunks(data, size=2))

    assert result == [
        [1, 2],
        [3, 4],
        [5, 6],
        [7, 8],
    ]


def test_chunks_splits_with_tail() -> None:
    data = [1, 2, 3, 4, 5, 6, 7]
    result = list(i2ls.chunks(data, size=3))

    assert result == [
        [1, 2, 3],
        [4, 5, 6],
        [7],
    ]
