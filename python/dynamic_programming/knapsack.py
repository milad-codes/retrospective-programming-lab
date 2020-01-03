"""0/1 knapsack: the most valuable subset of items within a weight capacity."""

from collections.abc import Sequence


def knapsack(weights: Sequence[int], values: Sequence[float], capacity: int) -> tuple[float, list[int]]:
    """Returns (best value, chosen item indices). O(n * capacity) — pseudo-polynomial in the capacity."""
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    n = len(weights)
    best = [[0.0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight, value = weights[i - 1], values[i - 1]
        for c in range(capacity + 1):
            best[i][c] = best[i - 1][c]
            if weight <= c and best[i - 1][c - weight] + value > best[i][c]:
                best[i][c] = best[i - 1][c - weight] + value
    chosen, c = [], capacity
    for i in range(n, 0, -1):
        if best[i][c] != best[i - 1][c]:
            chosen.append(i - 1)
            c -= weights[i - 1]
    return best[n][capacity], sorted(chosen)
