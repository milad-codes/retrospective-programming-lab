"""Dijkstra's shortest paths with a binary heap: O((V + E) log V). Weights must not be negative."""

import heapq
from collections.abc import Hashable, Mapping
from itertools import count

WeightedGraph = Mapping[Hashable, Mapping[Hashable, float]]


def shortest_paths(graph: WeightedGraph, source: Hashable) -> tuple[dict, dict]:
    """Returns (distance, parent) for every reachable node."""
    distance = {source: 0.0}
    parent: dict[Hashable, Hashable | None] = {source: None}
    tie = count()  # nodes need not be comparable, so the heap orders by (distance, insertion order)
    heap = [(0.0, next(tie), source)]
    while heap:
        dist, _, node = heapq.heappop(heap)
        if dist > distance[node]:
            continue  # stale entry: a shorter route was found after this one was pushed
        for neighbour, weight in graph.get(node, {}).items():
            if weight < 0:
                raise ValueError(f"negative weight on edge {node!r} -> {neighbour!r}")
            candidate = dist + weight
            if candidate < distance.get(neighbour, float("inf")):
                distance[neighbour] = candidate
                parent[neighbour] = node
                heapq.heappush(heap, (candidate, next(tie), neighbour))
    return distance, parent


def path_to(parent: dict, target: Hashable) -> list[Hashable] | None:
    if target not in parent:
        return None
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]
