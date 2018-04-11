import random
import unittest

from sorting.insertion import insertion_sort


class InsertionSortTest(unittest.TestCase):
    def test_sorts_random_lists_like_sorted(self):
        rng = random.Random(1)
        for size in range(0, 60):
            data = [rng.randrange(-50, 50) for _ in range(size)]
            self.assertEqual(insertion_sort(data), sorted(data))

    def test_is_stable(self):
        people = [("ada", 36), ("bob", 25), ("cy", 36), ("di", 25)]
        self.assertEqual(
            insertion_sort(people, key=lambda p: p[1]),
            [("bob", 25), ("di", 25), ("ada", 36), ("cy", 36)],
        )

    def test_leaves_the_input_untouched(self):
        data = [3, 1, 2]
        insertion_sort(data)
        self.assertEqual(data, [3, 1, 2])


if __name__ == "__main__":
    unittest.main()
