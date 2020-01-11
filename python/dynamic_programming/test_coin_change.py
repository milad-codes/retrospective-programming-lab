import unittest

from dynamic_programming.coin_change import fewest_coins, ways_to_pay


class CoinChangeTest(unittest.TestCase):
    def test_beats_the_greedy_choice(self):
        self.assertEqual(fewest_coins([1, 3, 4], 6), [3, 3])  # greedy would take 4 + 1 + 1

    def test_euro_coins(self):
        self.assertEqual(fewest_coins([1, 2, 5, 10, 20, 50, 100, 200], 388), [200, 100, 50, 20, 10, 5, 2, 1])

    def test_impossible_and_zero(self):
        self.assertIsNone(fewest_coins([4, 6], 7))
        self.assertEqual(fewest_coins([4, 6], 0), [])

    def test_ways_to_pay(self):
        self.assertEqual(ways_to_pay([1, 2, 5], 5), 4)
        self.assertEqual(ways_to_pay([2], 3), 0)
        self.assertEqual(ways_to_pay([1, 2, 5, 10, 20, 50, 100, 200], 200), 73682)


if __name__ == "__main__":
    unittest.main()
