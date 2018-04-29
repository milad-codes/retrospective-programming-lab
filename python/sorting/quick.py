"""Quicksort with a random pivot and three-way partitioning (Dutch national flag)."""

import random
from collections.abc import Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")


def quick_sort(
    items: Iterable[T], key: Callable[[T], Any] = lambda x: x, rng: random.Random | None = None
) -> list[T]:
    """Expected O(n log n); many equal keys stay cheap thanks to the three-way split. Not stable."""
    result = list(items)
    keys = [key(item) for item in result]
    _sort(result, keys, 0, len(result) - 1, rng or random.Random())
    return result


def _sort(items: list, keys: list, low: int, high: int, rng: random.Random) -> None:
    while low < high:
        pivot = keys[rng.randint(low, high)]
        lt, i, gt = low, low, high
        # invariant: [low, lt) < pivot, [lt, i) == pivot, (gt, high] > pivot
        while i <= gt:
            if keys[i] < pivot:
                _swap(items, keys, lt, i)
                lt += 1
                i += 1
            elif keys[i] > pivot:
                _swap(items, keys, i, gt)
                gt -= 1
            else:
                i += 1
        # recurse into the smaller side, loop on the larger one: O(log n) stack depth
        if lt - low < high - gt:
            _sort(items, keys, low, lt - 1, rng)
            low = gt + 1
        else:
            _sort(items, keys, gt + 1, high, rng)
            high = lt - 1


def _swap(items: list, keys: list, a: int, b: int) -> None:
    items[a], items[b] = items[b], items[a]
    keys[a], keys[b] = keys[b], keys[a]
