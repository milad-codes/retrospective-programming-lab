"""Heapsort on an implicit binary max-heap: O(n log n) in every case and O(1) extra space for the keys."""

from collections.abc import Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")


def heap_sort(items: Iterable[T], key: Callable[[T], Any] = lambda x: x) -> list[T]:
    result = list(items)
    keys = [key(item) for item in result]
    n = len(result)
    for start in range(n // 2 - 1, -1, -1):  # heapify bottom-up in O(n)
        _sift_down(result, keys, start, n)
    for end in range(n - 1, 0, -1):
        result[0], result[end] = result[end], result[0]
        keys[0], keys[end] = keys[end], keys[0]
        _sift_down(result, keys, 0, end)
    return result


def _sift_down(items: list, keys: list, root: int, size: int) -> None:
    while True:
        child = 2 * root + 1
        if child >= size:
            return
        if child + 1 < size and keys[child + 1] > keys[child]:
            child += 1
        if keys[root] >= keys[child]:
            return
        items[root], items[child] = items[child], items[root]
        keys[root], keys[child] = keys[child], keys[root]
        root = child
