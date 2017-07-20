import math
import unittest

from number_theory.gcd import extended_gcd, gcd, lcm, mod_inverse


class GcdTest(unittest.TestCase):
    def test_matches_the_standard_library(self):
        for a in range(-30, 31):
            for b in range(-30, 31):
                self.assertEqual(gcd(a, b), math.gcd(a, b))

    def test_lcm(self):
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(-4, 6), 12)
        self.assertEqual(lcm(0, 9), 0)

    def test_extended_gcd_gives_bezout_coefficients(self):
        for a, b in [(240, 46), (17, 5), (0, 7), (-12, 18), (99, 0)]:
            g, x, y = extended_gcd(a, b)
            self.assertEqual(g, math.gcd(a, b))
            self.assertEqual(a * x + b * y, g)

    def test_mod_inverse(self):
        self.assertEqual(mod_inverse(3, 11), 4)
        self.assertEqual(mod_inverse(-3, 11), 7)
        for a in range(1, 97):
            self.assertEqual(a * mod_inverse(a, 97) % 97, 1)

    def test_mod_inverse_rejects_non_coprime_values(self):
        with self.assertRaises(ValueError):
            mod_inverse(6, 9)
        with self.assertRaises(ValueError):
            mod_inverse(3, 1)


if __name__ == "__main__":
    unittest.main()
