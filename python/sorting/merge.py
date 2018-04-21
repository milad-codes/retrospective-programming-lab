"""Merge sort: O(n log n) in every case, stable, needs O(n) extra space."""

from collections.abc import Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")


def merge_sort(items: Iterable[T], key: Callable[[T], Any] = lambda x: x) -> list[T]:
    keyed = [(key(item), index, item) for index, item in enumerate(items)]
    return [item for _, _, item in _sort(keyed)]


def _sort(values: list) -> list:
    if len(values) <= 1:
        return values
    middle = len(values) // 2
    return _merge(_sort(values[:middle]), _sort(values[middle:]))


def _merge(left: list, right: list) -> list:
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        # <= takes from the left run first on ties, which is what makes the sort stable
        if left[i][0] <= right[j][0]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
