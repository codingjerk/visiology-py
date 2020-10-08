from typing import Any, Callable, Dict, Hashable, \
    Iterable, Iterator, List, Tuple, TypeVar


T = TypeVar("T")


def make_hashable(x: Any) -> Hashable:
    """
    Makes any value (generator, list, dictionary) hashable.
    Consumes generators, makes tuples from lists and dictionaries.
    """

    if isinstance(x, Hashable):
        return hash(x)

    if type(x) == list:
        return tuple(make_hashable(c) for c in x)

    if type(x) == set:
        return tuple(sorted(make_hashable(c) for c in x))

    if type(x) == dict:
        return tuple(sorted(make_hashable(c) for c in x.items()))

    raise NotImplementedError(
        f"Not make_hashable is not implemented for values of type {type(x)}"
    )


def identity(x: T) -> T:
    """
    Returns it's only argument
    Doesn't look usefull, but it wisely used in functional programming
    """

    return x


def duplicates(
    xs: Iterable[T],
    hash: Callable[[T], Hashable] = identity,
) -> Iterator[T]:
    """
    Returns generator of duplicates
    """

    seen = set()
    yielded = set()

    for x in xs:
        h = hash(x)

        if h in seen and h not in yielded:
            yield x
            yielded.add(h)

        seen.add(h)


def take(i: Iterator[T], size: int) -> List[T]:
    """
    Gets iterator `i` and return a list that contains maximum `size` elements
    """

    result = []

    for _ in range(size):
        try:
            result.append(next(i))
        except StopIteration:
            pass

    return result


def chunks(xs: Iterable[T], size: int) -> Iterator[List[T]]:
    """
    Splits iterable into chunks as lists with lenght `size`.
    """

    iterator = iter(xs)
    while chunk := take(iterator, size):
        yield chunk
