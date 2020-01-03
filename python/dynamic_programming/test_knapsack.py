import itertools
import random
import unittest

from dynamic_programming.knapsack import knapsack


class KnapsackTest(unittest.TestCase):
    def test_textbook_example(self):
        value, chosen = knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)
        self.assertEqual((value, chosen), (9, [1, 2]))

    def test_against_brute_force(self):
        rng = random.Random(13)
        for _ in range(100):
            n = rng.randint(0, 8)
            weights = [rng.randint(1, 10) for _ in range(n)]
            values = [rng.randint(0, 20) for _ in range(n)]
            capacity = rng.randint(0, 25)
            value, chosen = knapsack(weights, values, capacity)
            self.assertLessEqual(sum(weights[i] for i in chosen), capacity)
            self.assertEqual(sum(values[i] for i in chosen), value)
            best = max(
                sum(values[i] for i in subset)
                for size in range(n + 1)
                for subset in itertools.combinations(range(n), size)
                if sum(weights[i] for i in subset) <= capacity
            )
            self.assertEqual(value, best)


if __name__ == "__main__":
    unittest.main()
