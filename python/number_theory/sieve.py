"""Prime numbers by sieving, and factorisation by trial division."""


def primes_up_to(limit: int) -> list[int]:
    """Sieve of Eratosthenes: all primes p with 2 <= p <= limit, in O(n log log n)."""
    if limit < 2:
        return []
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    p = 2
    while p * p <= limit:
        if is_prime[p]:
            # multiples below p*p were already crossed out by smaller primes
            is_prime[p * p :: p] = bytes(len(range(p * p, limit + 1, p)))
        p += 1
    return [n for n, flag in enumerate(is_prime) if flag]


def prime_factors(n: int) -> list[int]:
    """Prime factors with multiplicity, ascending: prime_factors(360) == [2, 2, 2, 3, 3, 5]."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    factors = []
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors.append(n)
    return factors
