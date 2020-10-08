from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Hashable,
    Iterable,
    Iterator,
    List,
    Tuple,
    TypeVar,
)


__all__ = ["duplicates", "take", "chunks"]


T = TypeVar("T")


def duplicates(xs: Iterable[T]) -> Iterator[T]:
    """
    Returns generator of duplicates
    """

    seen: NohashSet[T] = NohashSet()
    yielded: NohashSet[T] = NohashSet()

    for x in xs:
        if x in seen and x not in yielded:
            yield x
            yielded.add(x)
        else:
            seen.add(x)


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

    chunk = take(iterator, size)
    while chunk:
        yield chunk
        chunk = take(iterator, size)


class NohashSet(Generic[T]):
    """
    Set-like collection with no `Hashable` restriction on elements
    """

    def __init__(self) -> None:
        self._real_buckets: Dict[int, List[T]] = dict()
        self._fallback_buckets: Dict[int, List[T]] = dict()

    def add(self, item: T) -> None:
        try:
            key = hash(item)
            if key not in self._real_buckets:
                self._real_buckets[key] = []

            self._real_buckets[key].append(item)
        except TypeError:
            pass

        key = hash(str(item))
        if key not in self._fallback_buckets:
            self._fallback_buckets[key] = []

        self._fallback_buckets[key].append(item)

    def __contains__(self, item: T) -> bool:
        if self._fast_real_buckets_check_not_contains(item):
            return False

        if self._fast_fallback_buckets_check_not_contains(item):
            return False

        if self._slow_real_buckets_check_contains(item):
            return True

        return self._slow_fallback_buckets_check_contains(item)

    def _fast_real_buckets_check_not_contains(self, item: T) -> bool:
        try:
            if hash(item) not in self._real_buckets:
                return True
        except TypeError:
            pass

        return False

    def _fast_fallback_buckets_check_not_contains(self, item: T) -> bool:
        return hash(str(item)) not in self._fallback_buckets

    def _slow_real_buckets_check_contains(self, item: T) -> bool:
        try:
            for item_in_bucket in self._real_buckets.get(hash(item), []):
                if item == item_in_bucket:
                    return True
        except TypeError:
            pass

        return False

    def _slow_fallback_buckets_check_contains(self, item: T) -> bool:
        for item_in_bucket in self._fallback_buckets.get(hash(str(item)), []):
            if item == item_in_bucket:
                return True

        return False
