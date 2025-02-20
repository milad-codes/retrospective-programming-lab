# Rate limiters

Two common ways to limit request rates, both with an injectable clock so the tests control time exactly.

| File | Algorithm | Allows | Memory per key |
| --- | --- | --- | --- |
| `token-bucket.ts` | token bucket with lazy refill | bursts up to the capacity, then the refill rate | two numbers |
| `sliding-window.ts` | sliding-window log | at most N events in **any** window of the given length | one timestamp per allowed event |

Each limiter tells the caller how long to wait (`waitTimeMs` / `retryAfterMs`), which maps directly to a `Retry-After`
header.

- The token-bucket test drives 10 seconds of traffic and expects exactly the initial burst plus the refill rate.
- The sliding-window test checks that no window of the configured length ever contains more than the limit, across
  5,000 random arrivals.

```bash
node --test typescript/rate-limiter/
```
