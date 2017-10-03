"""Modular exponentiation by repeated squaring."""


def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """base**exponent % modulus in O(log exponent) multiplications, without huge intermediate numbers."""
    if modulus < 1:
        raise ValueError("modulus must be positive")
    if exponent < 0:
        raise ValueError("negative exponents need a modular inverse; use number_theory.gcd.mod_inverse")
    result = 1 % modulus
    base %= modulus
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result
