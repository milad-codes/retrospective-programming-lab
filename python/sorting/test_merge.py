import random
import unittest

from sorting.merge import merge_sort


class MergeSortTest(unittest.TestCase):
    def test_sorts_random_lists_like_sorted(self):
        rng = random.Random(2)
        for size in [0, 1, 2, 3, 10, 100, 1000]:
            data = [rng.random() for _ in range(size)]
            self.assertEqual(merge_sort(data), sorted(data))

    def test_is_stable_with_a_key(self):
        words = ["pear", "fig", "apple", "kiwi", "plum", "date"]
        self.assertEqual(merge_sort(words, key=len), sorted(words, key=len))

    def test_does_not_compare_items_themselves(self):
        # dicts are not orderable; only the keys are compared
        rows = [{"n": 2}, {"n": 1}, {"n": 2}]
        self.assertEqual([r["n"] for r in merge_sort(rows, key=lambda r: r["n"])], [1, 2, 2])


if __name__ == "__main__":
    unittest.main()
