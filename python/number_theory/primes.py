"""Primality testing for large numbers (Miller–Rabin)."""

from number_theory.modpow import mod_pow

# With these bases Miller–Rabin is deterministic for every n < 3.3 * 10**24.
_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def is_prime(n: int) -> bool:
    """Exact for n < 3.3e24; beyond that a composite passing all 13 bases is astronomically unlikely."""
    if n < 2:
        return False
    for p in _BASES:
        if n % p == 0:
            return n == p
    # write n - 1 as d * 2**s with d odd
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _BASES:
        x = mod_pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True
