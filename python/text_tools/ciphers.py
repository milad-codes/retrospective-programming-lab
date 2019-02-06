"""Caesar and Vigenère ciphers over the Latin alphabet; other characters pass through unchanged."""

from itertools import cycle

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def _shift(char: str, amount: int) -> str:
    lower = char.lower()
    if lower not in ALPHABET:
        return char
    shifted = ALPHABET[(ALPHABET.index(lower) + amount) % 26]
    return shifted.upper() if char.isupper() else shifted


def caesar(text: str, shift: int) -> str:
    return "".join(_shift(char, shift) for char in text)


def vigenere(text: str, key: str, decrypt: bool = False) -> str:
    """The key advances only on letters, so spaces and punctuation don't consume key characters."""
    shifts = [ALPHABET.index(c) for c in key.lower() if c in ALPHABET]
    if not shifts:
        raise ValueError("the key needs at least one letter")
    sign = -1 if decrypt else 1
    stream = cycle(shifts)
    return "".join(_shift(c, sign * next(stream)) if c.lower() in ALPHABET else c for c in text)


def crack_caesar(ciphertext: str) -> int:
    """Guesses the shift by comparing letter frequencies with English (chi-squared)."""
    english = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 2.4,
               6.7, 7.5, 1.9, 0.095, 6.0, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2.0, 0.074]
    letters = [c for c in ciphertext.lower() if c in ALPHABET]
    if not letters:
        return 0

    def score(shift: int) -> float:
        counts = [0] * 26
        for c in letters:
            counts[(ALPHABET.index(c) - shift) % 26] += 1
        total = len(letters)
        return sum((counts[i] - total * english[i] / 100) ** 2 / (total * english[i] / 100) for i in range(26))

    return min(range(26), key=score)
