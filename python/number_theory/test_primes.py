import unittest

from number_theory.primes import is_prime
from number_theory.sieve import primes_up_to


class MillerRabinTest(unittest.TestCase):
    def test_agrees_with_the_sieve(self):
        primes = set(primes_up_to(100_000))
        for n in range(-5, 100_001):
            self.assertEqual(is_prime(n), n in primes, n)

    def test_carmichael_numbers_are_composite(self):
        for n in (561, 1105, 1729, 2465, 2821, 6601, 8911, 41041, 825265, 321197185):
            self.assertFalse(is_prime(n))

    def test_large_known_values(self):
        self.assertTrue(is_prime(2**61 - 1))  # Mersenne prime
        self.assertTrue(is_prime(1_000_000_007))
        self.assertFalse(is_prime(2**61 + 1))
        self.assertFalse(is_prime(3_215_031_751))  # strong pseudoprime to bases 2, 3, 5 and 7


if __name__ == "__main__":
    unittest.main()
