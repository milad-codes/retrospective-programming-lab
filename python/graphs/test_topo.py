import unittest

from graphs.topo import CycleError, topological_order


class TopologicalOrderTest(unittest.TestCase):
    def test_respects_every_edge(self):
        graph = {"shop": ["cook"], "cook": ["eat"], "wash": ["cook"], "eat": ["clean"]}
        order = topological_order(graph)
        for source, targets in graph.items():
            for target in targets:
                self.assertLess(order.index(source), order.index(target))
        self.assertEqual(set(order), {"shop", "cook", "eat", "wash", "clean"})

    def test_reports_the_nodes_on_a_cycle(self):
        with self.assertRaises(CycleError) as raised:
            topological_order({"a": ["b"], "b": ["c"], "c": ["a"], "start": ["a"]})
        self.assertEqual(raised.exception.remaining, {"a", "b", "c"})


if __name__ == "__main__":
    unittest.main()
