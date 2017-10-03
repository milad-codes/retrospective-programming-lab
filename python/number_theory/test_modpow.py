import random
import unittest

from number_theory.modpow import mod_pow


class ModPowTest(unittest.TestCase):
    def test_matches_builtin_pow(self):
        rng = random.Random(7)
        for _ in range(500):
            base, exponent, modulus = rng.randrange(-10**6, 10**6), rng.randrange(0, 10**4), rng.randrange(1, 10**9)
            self.assertEqual(mod_pow(base, exponent, modulus), pow(base, exponent, modulus))

    def test_edge_cases(self):
        self.assertEqual(mod_pow(5, 0, 1), 0)
        self.assertEqual(mod_pow(5, 0, 7), 1)
        self.assertEqual(mod_pow(0, 5, 7), 0)

    def test_fermat_little_theorem(self):
        for p in (5, 13, 101, 7919):
            for a in range(1, 20):
                self.assertEqual(mod_pow(a, p - 1, p), 1 if a % p else 0)

    def test_rejects_invalid_arguments(self):
        with self.assertRaises(ValueError):
            mod_pow(2, -1, 7)
        with self.assertRaises(ValueError):
            mod_pow(2, 3, 0)


if __name__ == "__main__":
    unittest.main()
