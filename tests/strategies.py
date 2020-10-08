from typing import Any
from hypothesis import strategies as st


def anything_simple() -> st.SearchStrategy[Any]:
    return st.one_of(
        st.integers(),
        st.binary(),
        st.booleans(),
        st.text(),
        st.characters(),
        st.dates(),
        st.datetimes(),
        st.floats(),
    )


def anything_nested() -> st.SearchStrategy[Any]:
    return st.one_of(
        anything_simple(),
        st.tuples(anything_simple()),
    )


def anything_iterable() -> st.SearchStrategy[Any]:
    return st.one_of(
        st.sets(anything_nested()),
        st.tuples(anything_nested()),
        st.lists(anything_nested()),
        st.dictionaries(anything_nested(), anything_nested()),
    )


def anything() -> st.SearchStrategy[Any]:
    return st.one_of(
        anything_nested(),
        anything_iterable(),
    )
