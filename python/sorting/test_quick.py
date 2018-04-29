import random
import sys
import unittest

from sorting.quick import quick_sort


class QuickSortTest(unittest.TestCase):
    def test_sorts_random_lists_like_sorted(self):
        rng = random.Random(3)
        for size in range(0, 200, 7):
            data = [rng.randrange(1000) for _ in range(size)]
            self.assertEqual(quick_sort(data, rng=random.Random(size)), sorted(data))

    def test_handles_many_duplicates_and_sorted_input_without_deep_recursion(self):
        limit = sys.getrecursionlimit()
        sys.setrecursionlimit(200)
        try:
            self.assertEqual(quick_sort([5] * 20_000), [5] * 20_000)
            self.assertEqual(quick_sort(list(range(20_000))), list(range(20_000)))
        finally:
            sys.setrecursionlimit(limit)

    def test_sorts_by_key(self):
        self.assertEqual(quick_sort(["bb", "a", "ccc"], key=len), ["a", "bb", "ccc"])


if __name__ == "__main__":
    unittest.main()
