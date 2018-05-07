import random
import unittest

from sorting.heap import heap_sort


class HeapSortTest(unittest.TestCase):
    def test_sorts_random_lists_like_sorted(self):
        rng = random.Random(4)
        for size in range(0, 300, 11):
            data = [rng.randrange(-500, 500) for _ in range(size)]
            self.assertEqual(heap_sort(data), sorted(data))

    def test_sorts_strings_by_key(self):
        words = ["Banana", "apple", "cherry"]
        self.assertEqual(heap_sort(words, key=str.lower), ["apple", "Banana", "cherry"])


if __name__ == "__main__":
    unittest.main()
