"""Insertion sort: simple, stable, and fast on short or nearly sorted input."""

from collections.abc import Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")


def insertion_sort(items: Iterable[T], key: Callable[[T], Any] = lambda x: x) -> list[T]:
    """O(n²) comparisons in general, O(n) when the input is already sorted. Stable."""
    result = list(items)
    for i in range(1, len(result)):
        current = result[i]
        current_key = key(current)
        j = i - 1
        # strict comparison keeps equal elements in their original order
        while j >= 0 and key(result[j]) > current_key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result
