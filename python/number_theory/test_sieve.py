import math
import unittest

from number_theory.sieve import prime_factors, primes_up_to


def naive_is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


class SieveTest(unittest.TestCase):
    def test_small_limits(self):
        self.assertEqual(primes_up_to(1), [])
        self.assertEqual(primes_up_to(2), [2])
        self.assertEqual(primes_up_to(30), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_agrees_with_trial_division(self):
        self.assertEqual(primes_up_to(2000), [n for n in range(2001) if naive_is_prime(n)])

    def test_counts_primes_below_one_million(self):
        self.assertEqual(len(primes_up_to(1_000_000)), 78_498)


class FactorTest(unittest.TestCase):
    def test_factors_multiply_back(self):
        for n in range(1, 3000):
            factors = prime_factors(n)
            self.assertEqual(math.prod(factors), n)
            self.assertTrue(all(naive_is_prime(f) for f in factors))
            self.assertEqual(factors, sorted(factors))

    def test_examples(self):
        self.assertEqual(prime_factors(360), [2, 2, 2, 3, 3, 5])
        self.assertEqual(prime_factors(97), [97])
        self.assertEqual(prime_factors(1), [])

    def test_rejects_non_positive_numbers(self):
        with self.assertRaises(ValueError):
            prime_factors(0)


if __name__ == "__main__":
    unittest.main()
