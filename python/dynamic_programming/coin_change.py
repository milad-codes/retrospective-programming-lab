"""Coin change: the fewest coins for an amount, and how many ways there are to pay it."""

from collections.abc import Sequence


def fewest_coins(coins: Sequence[int], amount: int) -> list[int] | None:
    """The coins used (largest first), or None if the amount can't be paid. Greedy fails for e.g. coins (1, 3, 4)."""
    inf = float("inf")
    best = [0] + [inf] * amount
    last_coin = [0] * (amount + 1)
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value and best[value - coin] + 1 < best[value]:
                best[value] = best[value - coin] + 1
                last_coin[value] = coin
    if best[amount] == inf:
        return None
    used, value = [], amount
    while value:
        used.append(last_coin[value])
        value -= last_coin[value]
    return sorted(used, reverse=True)


def ways_to_pay(coins: Sequence[int], amount: int) -> int:
    """Number of combinations (order doesn't matter): iterating coins in the outer loop avoids counting 1+2 and 2+1 twice."""
    ways = [1] + [0] * amount
    for coin in coins:
        for value in range(coin, amount + 1):
            ways[value] += ways[value - coin]
    return ways[amount]
