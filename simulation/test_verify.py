import unittest

from verify import instant


class InstantTest(unittest.TestCase):
    def test_z_and_zero_offset_are_the_same_instant(self):
        # CI's git prints "Z" in %aI where older versions print "+00:00"; the first CI run failed on that
        self.assertEqual(instant("2017-01-03T18:51:42Z"), instant("2017-01-03T18:51:42+00:00"))

    def test_other_offsets_compare_by_instant(self):
        self.assertEqual(instant("2026-10-29T17:39:31+01:00"), instant("2026-10-29T16:39:31Z"))
        self.assertNotEqual(instant("2017-01-03T18:51:42Z"), instant("2017-01-03T18:51:43Z"))


if __name__ == "__main__":
    unittest.main()
