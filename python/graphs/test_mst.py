import itertools
import random
import unittest

from graphs.mst import UnionFind, kruskal


def brute_force_mst(nodes, edges):
    best = float("inf")
    for subset in itertools.combinations(edges, len(nodes) - 1):
        sets = UnionFind(nodes)
        if all(sets.union(a, b) for _, a, b in subset):
            best = min(best, sum(w for w, _, _ in subset))
    return best


class KruskalTest(unittest.TestCase):
    def test_matches_brute_force(self):
        rng = random.Random(10)
        nodes = list(range(6))
        for _ in range(20):
            edges = [(rng.randint(1, 20), a, b) for a, b in itertools.combinations(nodes, 2)]
            total, chosen = kruskal(nodes, edges)
            self.assertEqual(len(chosen), len(nodes) - 1)
            self.assertEqual(total, brute_force_mst(nodes, edges))

    def test_spanning_forest_for_disconnected_graphs(self):
        total, chosen = kruskal("abcd", [(1, "a", "b"), (2, "c", "d")])
        self.assertEqual((total, len(chosen)), (3, 2))

    def test_union_find(self):
        sets = UnionFind(range(5))
        self.assertTrue(sets.union(0, 1))
        self.assertTrue(sets.union(1, 2))
        self.assertFalse(sets.union(0, 2))
        self.assertEqual(sets.find(2), sets.find(0))
        self.assertNotEqual(sets.find(3), sets.find(0))


if __name__ == "__main__":
    unittest.main()
