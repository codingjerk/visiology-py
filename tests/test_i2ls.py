from typing import Any, Collection, List, TypeVar

import pytest
from hypothesis import given

import i2ls
import tests.strategies as st


T = TypeVar("T")


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

    dups3 = list(i2ls.duplicates([{1: 2}, {3: 4}, {1: 2}, [5, 6], {7, 8}]))
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
