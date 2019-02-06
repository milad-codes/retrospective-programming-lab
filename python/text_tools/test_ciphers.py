import unittest

from text_tools.ciphers import caesar, crack_caesar, vigenere


class CipherTest(unittest.TestCase):
    def test_caesar_round_trip_keeps_case_and_punctuation(self):
        self.assertEqual(caesar("Hello, World!", 3), "Khoor, Zruog!")
        self.assertEqual(caesar(caesar("Hello, World!", 3), -3), "Hello, World!")
        self.assertEqual(caesar("xyz", 29), "abc")

    def test_vigenere_known_example(self):
        self.assertEqual(vigenere("ATTACK AT DAWN", "LEMON"), "LXFOPV EF RNHR")
        self.assertEqual(vigenere("LXFOPV EF RNHR", "LEMON", decrypt=True), "ATTACK AT DAWN")

    def test_vigenere_needs_a_letter_in_the_key(self):
        with self.assertRaises(ValueError):
            vigenere("text", "123")

    def test_crack_caesar_on_english_text(self):
        plain = "the quick brown fox jumps over the lazy dog while the sun is shining on the river"
        for shift in (1, 7, 13, 25):
            self.assertEqual(crack_caesar(caesar(plain, shift)), shift)


if __name__ == "__main__":
    unittest.main()
