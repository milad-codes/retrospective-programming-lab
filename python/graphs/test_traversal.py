import unittest

from graphs.traversal import bfs_path, connected_components, dfs_order

GRID = {  # 3x3 grid, 4-neighbourhood
    (r, c): [(r + dr, c + dc) for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)) if 0 <= r + dr < 3 and 0 <= c + dc < 3]
    for r in range(3)
    for c in range(3)
}


class TraversalTest(unittest.TestCase):
    def test_bfs_finds_a_shortest_path(self):
        path = bfs_path(GRID, (0, 0), (2, 2))
        self.assertEqual(len(path), 5)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))
        for a, b in zip(path, path[1:]):
            self.assertIn(b, GRID[a])

    def test_bfs_unreachable_and_trivial(self):
        graph = {"a": ["b"], "b": [], "c": []}
        self.assertIsNone(bfs_path(graph, "a", "c"))
        self.assertEqual(bfs_path(graph, "a", "a"), ["a"])

    def test_dfs_order_and_deep_graphs(self):
        graph = {1: [2, 3], 2: [4], 3: [], 4: []}
        self.assertEqual(dfs_order(graph, 1), [1, 2, 4, 3])
        chain = {i: [i + 1] for i in range(100_000)}
        self.assertEqual(len(dfs_order(chain, 0)), 100_001)

    def test_connected_components(self):
        graph = {1: [2], 2: [1], 3: [4], 4: [3], 5: []}
        self.assertEqual(connected_components(graph), [{1, 2}, {3, 4}, {5}])


if __name__ == "__main__":
    unittest.main()
