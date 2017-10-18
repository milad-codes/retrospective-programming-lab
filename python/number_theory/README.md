# Number theory

Small, exact implementations of the number-theory tools that keep coming back in programming exercises.

| File | What it does | Cost |
| --- | --- | --- |
| `gcd.py` | Euclid's `gcd`, `lcm`, `extended_gcd` (Bézout coefficients) and `mod_inverse` | O(log min(a, b)) |
| `sieve.py` | `primes_up_to(n)` with the sieve of Eratosthenes; `prime_factors(n)` by trial division | O(n log log n); O(√n) |
| `modpow.py` | `mod_pow` by repeated squaring | O(log e) multiplications |
| `primes.py` | `is_prime` with deterministic Miller–Rabin bases | O(k log³ n) |

The tests compare against the standard library (`math.gcd`, `pow`) or against a brute-force version on every input in a
range, rather than checking a few hand-picked examples. Run them from the `python/` folder:

```bash
python3 -m unittest discover -s number_theory -t .
```

Why the sieve starts crossing out at `p * p`: every smaller multiple `k * p` with `k < p` has a prime factor smaller
than `p` and was already removed.
