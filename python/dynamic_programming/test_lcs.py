import itertools
import random
import unittest

from dynamic_programming.lcs import longest_common_subsequence


def is_subsequence(small: str, big: str) -> bool:
    it = iter(big)
    return all(char in it for char in small)


def brute_force_length(a: str, b: str) -> int:
    for size in range(len(a), -1, -1):
        if any(is_subsequence("".join(c), b) for c in itertools.combinations(a, size)):
            return size
    return 0


class LcsTest(unittest.TestCase):
    def test_classic_example(self):
        self.assertEqual(len(longest_common_subsequence("ABCBDAB", "BDCABA")), 4)

    def test_against_brute_force(self):
        rng = random.Random(12)
        for _ in range(150):
            a = "".join(rng.choice("xyz") for _ in range(rng.randint(0, 7)))
            b = "".join(rng.choice("xyz") for _ in range(rng.randint(0, 7)))
            result = longest_common_subsequence(a, b)
            self.assertTrue(is_subsequence(result, a) and is_subsequence(result, b))
            self.assertEqual(len(result), brute_force_length(a, b))


if __name__ == "__main__":
    unittest.main()
