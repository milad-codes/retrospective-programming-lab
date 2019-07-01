"""Topological ordering with Kahn's algorithm; reports a cycle instead of returning a partial order."""

from collections import deque
from collections.abc import Hashable, Mapping, Sequence


class CycleError(ValueError):
    def __init__(self, remaining: set) -> None:
        super().__init__(f"the graph has a cycle among: {sorted(map(str, remaining))}")
        self.remaining = remaining


def topological_order(graph: Mapping[Hashable, Sequence[Hashable]]) -> list[Hashable]:
    """Edges point from a prerequisite to what depends on it. Ties follow the mapping's order."""
    nodes = list(dict.fromkeys([*graph, *(m for targets in graph.values() for m in targets)]))
    indegree = {node: 0 for node in nodes}
    for targets in graph.values():
        for target in targets:
            indegree[target] += 1
    ready = deque(node for node in nodes if indegree[node] == 0)
    order = []
    while ready:
        node = ready.popleft()
        order.append(node)
        for target in graph.get(node, ()):
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    if len(order) != len(nodes):
        raise CycleError({node for node in nodes if indegree[node] > 0})
    return order
