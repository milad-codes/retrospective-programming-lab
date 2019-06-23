import itertools
import random
import unittest

from graphs.dijkstra import path_to, shortest_paths


def brute_force(graph, source, target):
    nodes = [n for n in graph if n not in (source, target)]
    best = float("inf")
    for size in range(len(nodes) + 1):
        for middle in itertools.permutations(nodes, size):
            route = (source, *middle, target)
            if all(b in graph[a] for a, b in zip(route, route[1:])):
                best = min(best, sum(graph[a][b] for a, b in zip(route, route[1:])))
    return best


class DijkstraTest(unittest.TestCase):
    def test_textbook_example(self):
        graph = {"a": {"b": 7, "c": 9, "f": 14}, "b": {"c": 10, "d": 15}, "c": {"d": 11, "f": 2},
                 "d": {"e": 6}, "e": {}, "f": {"e": 9}}
        distance, parent = shortest_paths(graph, "a")
        self.assertEqual(distance["e"], 20)
        self.assertEqual(path_to(parent, "e"), ["a", "c", "f", "e"])

    def test_matches_brute_force_on_small_random_graphs(self):
        rng = random.Random(9)
        for _ in range(40):
            nodes = range(6)
            graph = {n: {m: rng.randint(0, 9) for m in nodes if m != n and rng.random() < 0.4} for n in nodes}
            distance, _ = shortest_paths(graph, 0)
            for target in nodes[1:]:
                self.assertEqual(distance.get(target, float("inf")), brute_force(graph, 0, target))

    def test_unreachable_and_negative_weights(self):
        self.assertIsNone(path_to(shortest_paths({"a": {}}, "a")[1], "z"))
        with self.assertRaises(ValueError):
            shortest_paths({"a": {"b": -1}, "b": {}}, "a")


if __name__ == "__main__":
    unittest.main()
