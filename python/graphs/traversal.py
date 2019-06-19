"""Breadth-first and depth-first traversal on unweighted graphs."""

from collections import deque
from collections.abc import Hashable, Mapping, Sequence

Graph = Mapping[Hashable, Sequence[Hashable]]


def bfs_path(graph: Graph, start: Hashable, goal: Hashable) -> list[Hashable] | None:
    """Shortest path by number of edges, or None when the goal is unreachable."""
    parents: dict[Hashable, Hashable | None] = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parents[node]
            return path[::-1]
        for neighbour in graph.get(node, ()):
            if neighbour not in parents:
                parents[neighbour] = node
                queue.append(neighbour)
    return None


def dfs_order(graph: Graph, start: Hashable) -> list[Hashable]:
    """Iterative depth-first pre-order that visits neighbours in the listed order (no recursion limit)."""
    seen, order, stack = set(), [], [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        stack.extend(reversed(graph.get(node, ())))
    return order


def connected_components(graph: Graph) -> list[set[Hashable]]:
    """Components of an undirected graph given with both edge directions."""
    seen: set[Hashable] = set()
    components = []
    for node in graph:
        if node not in seen:
            component = set(dfs_order(graph, node))
            seen |= component
            components.append(component)
    return components
