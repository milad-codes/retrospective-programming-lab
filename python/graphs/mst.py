"""Minimum spanning tree with Kruskal's algorithm and a union-find with path compression and union by size."""

from collections.abc import Hashable, Iterable


class UnionFind:
    def __init__(self, items: Iterable[Hashable] = ()) -> None:
        self._parent: dict[Hashable, Hashable] = {}
        self._size: dict[Hashable, int] = {}
        for item in items:
            self.add(item)

    def add(self, item: Hashable) -> None:
        if item not in self._parent:
            self._parent[item] = item
            self._size[item] = 1

    def find(self, item: Hashable) -> Hashable:
        root = item
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[item] != root:  # path compression
            self._parent[item], item = root, self._parent[item]
        return root

    def union(self, a: Hashable, b: Hashable) -> bool:
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        if self._size[root_a] < self._size[root_b]:
            root_a, root_b = root_b, root_a
        self._parent[root_b] = root_a
        self._size[root_a] += self._size[root_b]
        return True


def kruskal(nodes: Iterable[Hashable], edges: Iterable[tuple[float, Hashable, Hashable]]):
    """Returns (total weight, chosen edges). For a disconnected graph this is a minimum spanning forest."""
    sets = UnionFind(nodes)
    chosen = []
    for weight, a, b in sorted(edges, key=lambda edge: edge[0]):
        if sets.union(a, b):
            chosen.append((weight, a, b))
    return sum(weight for weight, _, _ in chosen), chosen
