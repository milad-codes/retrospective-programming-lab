"""Greatest common divisor and the things it makes possible."""


def gcd(a: int, b: int) -> int:
    """Euclid's algorithm. gcd(0, 0) is 0 by convention; the result is never negative."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Least common multiple; 0 if either argument is 0."""
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Returns (g, x, y) with a*x + b*y == g == gcd(a, b) (Bézout coefficients), iteratively."""
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    if old_r < 0:
        old_r, old_x, old_y = -old_r, -old_x, -old_y
    return old_r, old_x, old_y


def mod_inverse(a: int, m: int) -> int:
    """The x in [0, m) with a*x ≡ 1 (mod m). Raises ValueError when a and m are not coprime."""
    if m <= 1:
        raise ValueError("modulus must be greater than 1")
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {m}")
    return x % m
